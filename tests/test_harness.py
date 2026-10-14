"""Automated acceptance tests for TaskAnalyzer."""

from datetime import datetime, timedelta, timezone

import pytest

from src.task_analyzer import TaskValidationError, analyze_tasks


UTC = timezone.utc
NOW = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)


def task(
    task_id: int,
    *,
    created: datetime = NOW - timedelta(hours=10),
    completed: datetime | None = NOW - timedelta(hours=2),
    deadline: datetime = NOW - timedelta(hours=1),
    priority: str = "media",
    status: str = "concluida",
) -> dict[str, object]:
    """Build a task fixture with sensible defaults."""
    return {
        "id_tarefa": task_id,
        "titulo": f"Tarefa {task_id}",
        "data_criacao": created,
        "data_conclusao": completed,
        "prazo": deadline,
        "prioridade": priority,
        "status": status,
    }


def test_calculo_metricas_sucesso() -> None:
    """Validate totals, completion averages and delay rates."""
    tasks = [
        task(1, created=NOW - timedelta(hours=10), completed=NOW - timedelta(hours=2),
             deadline=NOW - timedelta(hours=3), priority="alta"),
        task(2, created=NOW - timedelta(hours=8), completed=NOW - timedelta(hours=4),
             deadline=NOW - timedelta(hours=2), priority="baixa"),
        task(3, completed=None, deadline=NOW + timedelta(hours=3),
             priority="media", status="pendente"),
        task(4, completed=None, deadline=NOW - timedelta(hours=1),
             priority="alta", status="pendente"),
    ]

    result = analyze_tasks(tasks)

    assert result["total_tarefas"] == 4
    assert result["total_concluidas"] == 2
    assert result["total_pendentes"] == 2
    assert result["tempo_medio_conclusao_horas"] == 6.0
    assert result["tempo_medio_por_prioridade"] == {
        "baixa": 4.0, "media": 0.0, "alta": 8.0
    }
    assert result["taxa_atraso_percentual"] == 50.0
    assert result["taxa_atraso_por_prioridade"] == {
        "baixa": 0.0, "media": 0.0, "alta": 100.0
    }
    assert result["indicadores_por_prioridade"]["alta"]["quantidade_tarefas"] == 2


def test_data_inconsistente_gera_task_validation_error() -> None:
    """Reject a completion timestamp earlier than task creation."""
    invalid = task(
        10,
        created=NOW,
        completed=NOW - timedelta(minutes=1),
        deadline=NOW + timedelta(hours=1),
    )

    with pytest.raises(TaskValidationError, match="anterior a data_criacao"):
        analyze_tasks([invalid])


def test_lista_vazia_retorna_indicadores_zerados() -> None:
    """Return zero metrics for an empty task list."""
    result = analyze_tasks([])

    assert result["total_tarefas"] == 0
    assert result["total_concluidas"] == 0
    assert result["total_pendentes"] == 0
    assert result["tempo_medio_conclusao_horas"] == 0.0
    assert result["taxa_atraso_percentual"] == 0.0
    assert result["tempo_medio_por_prioridade"] == {
        "baixa": 0.0, "media": 0.0, "alta": 0.0
    }


def test_apenas_tarefas_pendentes_nao_divide_por_zero() -> None:
    """Return zero averages when no task has been completed."""
    result = analyze_tasks([
        task(1, completed=None, status="pendente", deadline=NOW + timedelta(days=1)),
        task(2, completed=None, status="pendente", priority="alta",
             deadline=NOW + timedelta(days=1)),
    ])

    assert result["total_tarefas"] == 2
    assert result["total_concluidas"] == 0
    assert result["total_pendentes"] == 2
    assert result["tempo_medio_conclusao_horas"] == 0.0
    assert result["tempo_medio_por_prioridade"]["alta"] == 0.0


def test_status_invalido_nao_entra_nos_indicadores() -> None:
    """Ignore tasks whose status is outside the contract."""
    result = analyze_tasks([task(1, status="em_andamento")])
    assert result["total_tarefas"] == 0
