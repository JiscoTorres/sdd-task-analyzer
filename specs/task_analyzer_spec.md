# Especificação SDD — TaskAnalyzer

## 1. Propósito
Analisar tarefas e calcular indicadores objetivos de produtividade, incluindo duração média de conclusão, atrasos e métricas por prioridade. Não fazem parte do escopo persistência, interface gráfica, APIs externas ou autenticação.

## 2. Contrato de entrada
Cada tarefa é um dicionário com os seguintes campos:

| Campo | Tipo esperado | Obrigatório | Regra |
|---|---|---:|---|
| `id_tarefa` | `int` | Sim | Identificador maior que zero |
| `titulo` | `str` | Sim | Não vazio |
| `data_criacao` | `datetime` | Sim | Data/hora com fuso UTC |
| `data_conclusao` | `datetime` ou `None` | Não | `None` para tarefas não concluídas |
| `prazo` | `datetime` | Sim | Data/hora com fuso UTC |
| `prioridade` | `str` | Sim | `baixa`, `media` ou `alta` |
| `status` | `str` | Sim | `concluida`, `pendente` ou `cancelada` |

## 3. Regras de negócio
- Considerar apenas tarefas com status válido nos indicadores.
- O tempo de conclusão é `data_conclusao - data_criacao`, em horas, arredondado para duas casas decimais.
- A média de conclusão considera somente tarefas com status `concluida`.
- Uma tarefa concluída está atrasada quando `data_conclusao > prazo`.
- Uma tarefa pendente está atrasada quando o instante UTC atual é posterior ao prazo.
- Tarefas canceladas não entram no cálculo da taxa de atraso.
- Taxas são percentuais de tarefas atrasadas entre tarefas válidas não canceladas; se não houver denominador, retornar `0.0`.
- A lista vazia deve retornar indicadores zerados sem exceção.
- Datas devem ser UTC; não misturar datas com e sem fuso.
- Arredondar tempos e percentuais para duas casas decimais.

## 4. Saída
A função `analyze_tasks` retorna um dicionário contendo:
- `total_tarefas`: quantidade de tarefas com status válido e estrutura válida;
- `total_concluidas`: quantidade de tarefas concluídas válidas;
- `total_pendentes`: quantidade de tarefas pendentes válidas;
- `tempo_medio_conclusao_horas`: média geral das tarefas concluídas;
- `tempo_medio_por_prioridade`: médias por prioridade;
- `taxa_atraso_percentual`: taxa geral de atraso;
- `taxa_atraso_por_prioridade`: taxas de atraso por prioridade;
- `indicadores_por_prioridade`: métricas agregadas para `baixa`, `media` e `alta`.

Médias sem tarefas concluídas retornam `0.0`. Prioridades sem tarefas válidas retornam métricas zeradas.

## 5. Exceção e diferença entre fases
A especificação da Fase 1 descreve datas inconsistentes como excluídas dos cálculos e reportadas via log. O enunciado da Fase 2 solicita especificamente validar que `data_conclusao < data_criacao` dispara `TaskValidationError`. Para atender ao critério explícito do Test Harness da Fase 2, esta implementação levanta `TaskValidationError` quando encontra uma conclusão anterior à criação. Esta decisão deve ser declarada no relatório e pode ser confirmada com o docente.

## 6. Cenários de aceite
1. Sucesso: verificar totais, médias gerais e por prioridade e taxas de atraso.
2. Erro: conclusão anterior à criação gera `TaskValidationError`.
3. Borda: lista vazia ou tarefas apenas pendentes retorna médias `0.0`, sem divisão por zero.
