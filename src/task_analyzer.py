"""Analyze task completion metrics according to the TaskAnalyzer SDD contract."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

VALID_PRIORITIES = ("baixa", "media", "alta")
VALID_STATUSES = ("concluida", "pendente", "cancelada")


class TaskValidationError(ValueError):
    """Raised when a task violates a required business validation rule."""


def _is_utc_datetime(value: object) -> bool:
    """Return whether a value is a timezone-aware UTC datetime."""
    return (
        isinstance(value, datetime)
        and value.tzinfo is not None
        and value.utcoffset() == timezone.utc.utcoffset(value)
    )


def _validate_task(task: dict[str, Any], index: int) -> None:
    """Validate the required structure and temporal consistency of a task.

    Args:
        task: Task dictionary to validate.
        index: Position of the task in the input sequence.

    Raises:
        TaskValidationError: If required fields or date rules are invalid.
    """
    required = (
        "id_tarefa",
        "titulo",
        "data_criacao",
        "data_conclusao",
        "prazo",
        "prioridade",
        "status",
    )
    missing = [field for field in required if field not in task]
    if missing:
        raise TaskValidationError(
            f"Tarefa na posição {index}: campos ausentes: {', '.join(missing)}."
        )

    if not isinstance(task["id_tarefa"], int) or isinstance(task["id_tarefa"], bool):
        raise TaskValidationError(f"Tarefa na posição {index}: id_tarefa deve ser inteiro.")
    if task["id_tarefa"] <= 0:
        raise TaskValidationError(f"Tarefa na posição {index}: id_tarefa deve ser maior que zero.")
    if not isinstance(task["titulo"], str) or not task["titulo"].strip():
        raise TaskValidationError(f"Tarefa na posição {index}: titulo não pode ser vazio.")

    for field in ("data_criacao", "prazo"):
        if not _is_utc_datetime(task[field]):
            raise TaskValidationError(
                f"Tarefa na posição {index}: {field} deve ser datetime com fuso UTC."
            )

    conclusion = task["data_conclusao"]
    if conclusion is not None and not _is_utc_datetime(conclusion):
        raise TaskValidationError(
            f"Tarefa na posição {index}: data_conclusao deve ser datetime UTC ou None."
        )
    if conclusion is not None and conclusion < task["data_criacao"]:
        logger.error("Data inconsistente na tarefa id=%s", task["id_tarefa"])
        raise TaskValidationError(
            f"Tarefa {task['id_tarefa']}: data_conclusao anterior a data_criacao."
        )

    if task["prioridade"] not in VALID_PRIORITIES:
        raise TaskValidationError(
            f"Tarefa na posição {index}: prioridade deve ser baixa, media ou alta."
        )
    if task["status"] not in VALID_STATUSES:
        logger.warning("Tarefa ignorada por status inválido na posição %s", index)


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate overall and priority-specific task metrics.

    Args:
        tasks: List of task dictionaries matching the SDD input contract.

    Returns:
        Dictionary with totals, average completion time and delay percentages.

    Raises:
        TaskValidationError: If a task has inconsistent dates or malformed fields.
    """
    if not isinstance(tasks, list):
        raise TaskValidationError("A entrada deve ser uma lista de tarefas.")

    valid_tasks: list[dict[str, Any]] = []
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise TaskValidationError(f"Tarefa na posição {index} deve ser um dicionário.")
        _validate_task(task, index)
        if task["status"] in VALID_STATUSES:
            valid_tasks.append(task)

    now = datetime.now(timezone.utc)
    priorities: dict[str, list[dict[str, Any]]] = {
        priority: [task for task in valid_tasks if task["prioridade"] == priority]
        for priority in VALID_PRIORITIES
    }

    def completion_hours(task: dict[str, Any]) -> float:
        """Calculate completion duration for a completed task."""
        conclusion = task["data_conclusao"]
        assert isinstance(conclusion, datetime)
        return (conclusion - task["data_criacao"]).total_seconds() / 3600

    def average_completion(items: list[dict[str, Any]]) -> float:
        """Return the average duration of completed tasks, or zero."""
        completed = [task for task in items if task["status"] == "concluida"]
        if not completed:
            return 0.0
        return round(sum(completion_hours(task) for task in completed) / len(completed), 2)

    def delay_rate(items: list[dict[str, Any]]) -> float:
        """Return the delay percentage among completed and pending tasks."""
        eligible = [
            task for task in items if task["status"] in ("concluida", "pendente")
        ]
        if not eligible:
            return 0.0
        delayed = 0
        for task in eligible:
            reference_time = (
                task["data_conclusao"]
                if task["status"] == "concluida"
                else now
            )
            assert isinstance(reference_time, datetime)
            if reference_time > task["prazo"]:
                delayed += 1
        return round((delayed / len(eligible)) * 100, 2)

    by_priority: dict[str, dict[str, int | float]] = {}
    average_by_priority: dict[str, float] = {}
    delay_by_priority: dict[str, float] = {}
    for priority, items in priorities.items():
        completed_count = sum(task["status"] == "concluida" for task in items)
        pending_count = sum(task["status"] == "pendente" for task in items)
        average = average_completion(items)
        rate = delay_rate(items)
        average_by_priority[priority] = average
        delay_by_priority[priority] = rate
        by_priority[priority] = {
            "quantidade_tarefas": len(items),
            "total_concluidas": completed_count,
            "total_pendentes": pending_count,
            "tempo_medio_conclusao_horas": average,
            "taxa_atraso_percentual": rate,
        }

    logger.info("Análise concluída: %s tarefas válidas", len(valid_tasks))
    return {
        "total_tarefas": len(valid_tasks),
        "total_concluidas": sum(task["status"] == "concluida" for task in valid_tasks),
        "total_pendentes": sum(task["status"] == "pendente" for task in valid_tasks),
        "tempo_medio_conclusao_horas": average_completion(valid_tasks),
        "tempo_medio_por_prioridade": average_by_priority,
        "taxa_atraso_percentual": delay_rate(valid_tasks),
        "taxa_atraso_por_prioridade": delay_by_priority,
        "indicadores_por_prioridade": by_priority,
    }
