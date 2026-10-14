# CONTEXT_RULES — TaskAnalyzer

## Diretrizes arquiteturais obrigatórias
- Usar Python 3.11 ou superior.
- Usar type hints em todas as funções e métodos.
- Aplicar responsabilidade única (SRP), PEP 8 e código limpo.
- Usar docstrings no estilo Google para módulo, classes e funções.
- Manter funções pequenas, coesas e com propósito único.
- Usar exceções específicas e mensagens claras.
- Usar o módulo padrão `logging` para registrar eventos relevantes.
- Usar nomes descritivos e código legível e manutenível.

## Proibições explícitas
- Não usar bibliotecas externas além das dependências autorizadas.
- Não alterar a estrutura de pastas especificada.
- Não persistir dados em arquivos ou bancos de dados.
- Não alterar a assinatura da função pública sem autorização.
- Não introduzir funcionalidades não especificadas.
- Não duplicar código sem necessidade.
- Manter testes automatizados correspondentes ao comportamento implementado.

## Regras de interação e homologação com IA
- Fornecer a especificação completa e estas regras antes de solicitar código.
- Confirmar a compreensão do contrato antes de aceitar a solução.
- Pedir explicações quando houver dúvida.
- Revisar criticamente todo código gerado antes de realizar commit.
- Rejeitar código que viole o contrato ou as proibições.
- Executar todos os testes automatizados e revisar manualmente casos de borda.
- A decisão final de homologação permanece humana.

## Decisão específica da Fase 2
O enunciado intermediário nomeia a exceção `TaskValidationError` e solicita que datas inconsistentes (conclusão anterior à criação) disparem essa exceção. Esta regra específica foi adotada no código e nos testes da Fase 2, embora a Fase 1 também descreva exclusão e logging dessas tarefas. Não ocultar essa divergência: documentá-la e, se necessário, solicitar confirmação ao professor.
