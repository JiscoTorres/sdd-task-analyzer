# Guia de finalização da Fase 2 — TaskAnalyzer

Este pacote contém a implementação e os testes do projeto. Você ainda precisa publicar no seu GitHub, abrir o Pull Request, capturar os prints reais, gravar o vídeo e enviar o PDF final pela plataforma da disciplina.

## 1. Antes de publicar
1. Abra o `CONTEXT_RULES.md` e `specs/task_analyzer_spec.md`.
2. Leia `src/task_analyzer.py` e `tests/test_harness.py` para conseguir explicar o que fazem.
3. Confira a decisão documentada sobre a divergência entre a Fase 1 e a Fase 2 quanto a datas inconsistentes.

## 2. Preparar Python no Windows
No PowerShell, entre na pasta do projeto e execute:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```
O resultado esperado é `5 passed`. Se `py -3.11` não existir, instale Python 3.11+ ou use uma versão compatível já instalada.

## 3. Criar o repositório remoto
1. Acesse https://github.com/new
2. Nome: `sdd-task-analyzer`
3. Marque Public.
4. Deixe desmarcados README, .gitignore e licença (os arquivos já estão no projeto).
5. Crie o repositório e copie a URL HTTPS.

## 4. Git: primeiro envio
No PowerShell, dentro da pasta do projeto:
```powershell
git init -b main
git add README.md CONTEXT_RULES.md specs .gitignore requirements.txt
git commit -m "docs: adiciona especificacao SDD e regras de contexto"
git remote add origin https://github.com/SEU-USUARIO/sdd-task-analyzer.git
git push -u origin main
```
Troque `SEU-USUARIO` pela sua conta do GitHub. Se o Git pedir identificação:
```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu-email-do-github"
```

## 5. Criar branch de implementação e abrir PR
```powershell
git switch -c feature/task-analyzer-impl
git add src tests
git commit -m "feat: implementa TaskAnalyzer e testes automatizados"
git push -u origin feature/task-analyzer-impl
```
Abra o repositório no navegador. O GitHub normalmente mostra o botão **Compare & pull request**. Crie um PR de `feature/task-analyzer-impl` para `main`.
- Título sugerido: `feat: implementa TaskAnalyzer com pytest`
- Descrição sugerida:
  - Implementa métricas gerais e por prioridade.
  - Adiciona validação de datas e `TaskValidationError`.
  - Adiciona testes para sucesso, erro e casos de borda.
  - Validação local: `python -m pytest -v` — 5 testes aprovados.
  - Revisão humana: conferir contrato SDD, regras de contexto e resultados dos testes.
Revise os arquivos e só então faça o merge. Não declare um PR como revisado se você não tiver feito a revisão.

## 6. Prompt utilizado para geração/revisão por IA
Registre o prompt real que você usou. Sugestão:
> Leia integralmente `CONTEXT_RULES.md` e `specs/task_analyzer_spec.md` antes de alterar o código. Resuma o contrato e liste possíveis ambiguidades. Implemente apenas o comportamento descrito, usando Python 3.11+, type hints em todas as funções, docstrings Google style, logging da biblioteca padrão e exceção `TaskValidationError`. Não altere a estrutura de pastas, não use bibliotecas não autorizadas, não persista dados e não invente funcionalidades. Gere/atualize testes pytest para os cenários de sucesso, erro e borda. Explique como cada regra foi atendida e sinalize divergências entre a Fase 1 e a Fase 2 em vez de escondê-las.

Importante: descreva no relatório quais partes foram geradas com IA, o que você revisou e o que alterou. Não afirme que a IA evitou todas as alucinações; dê exemplos verificáveis.

## 7. Evidências obrigatórias
Capture evidências reais no seu computador/GitHub:
- Terminal com `python -m pytest -v` e `5 passed`.
- Árvore de arquivos no GitHub.
- Página do Pull Request aberto ou merged.
- Link público do repositório.
- Link do vídeo do YouTube (Público ou Não listado).

## 8. Roteiro de vídeo de 5 minutos
- 0:00–0:40 — Apresentar o objetivo do TaskAnalyzer e o contrato SDD.
- 0:40–1:30 — Mostrar a estrutura do repositório e `CONTEXT_RULES.md`.
- 1:30–2:20 — Mostrar a função `analyze_tasks` e explicar totais, médias e atrasos.
- 2:20–3:20 — Executar `python -m pytest -v` e mostrar todos os testes aprovados.
- 3:20–4:20 — Mostrar branch e Pull Request, explicando a revisão humana.
- 4:20–5:00 — Explicar a divergência de datas inconsistentes e como foi documentada.

Grave na horizontal, com áudio e câmera visíveis, conforme o enunciado.

## 9. PDF final da entrega
Monte um PDF com:
1. Nome e disciplina.
2. Link ativo do repositório público.
3. Print real dos testes aprovados.
4. Print real da árvore do GitHub.
5. Print real do Pull Request.
6. Relato dos prompts utilizados e da revisão humana.
7. Link do vídeo.
8. Observação sobre a divergência entre as regras de datas das fases, se não houver esclarecimento prévio do docente.

Não use capturas ilustrativas como se fossem evidências reais. Os prints devem vir da sua execução e do seu repositório.
