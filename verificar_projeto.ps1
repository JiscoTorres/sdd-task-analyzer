# Rode este script no PowerShell dentro da pasta sdd-task-analyzer.
$ErrorActionPreference = "Stop"
Write-Host "== Python ==" -ForegroundColor Cyan
python --version
Write-Host "`n== Testes ==" -ForegroundColor Cyan
python -m pytest -v
if ($LASTEXITCODE -ne 0) {
    throw "Os testes falharam. Corrija antes de versionar."
}
Write-Host "`nTestes aprovados. Agora siga GUIA_FINALIZACAO.md para publicar no GitHub." -ForegroundColor Green
