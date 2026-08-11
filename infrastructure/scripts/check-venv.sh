#!/usr/bin/env bash

cd "$(dirname "$0")/../backend" || exit 1

if [ ! -d ".venv" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado em backend/.venv"
    echo "💡 Correção: Execute 'python -m venv .venv' dentro da pasta backend/"
    exit 1
fi

if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "❌ Erro: Ambiente virtual não está ativo."
    echo "💡 Correção: Certifique-se de ter instalado o direnv e executado 'direnv allow' na pasta backend/, ou ative manualmente com 'source .venv/bin/activate'."
    exit 1
fi

PYTHON_EXEC=$(command -v python)
if [[ "$PYTHON_EXEC" != *".venv"* ]]; then
    echo "❌ Erro: O executável do Python não pertence ao .venv!"
    echo "Python atual: $PYTHON_EXEC"
    exit 1
fi

if ! command -v pip >/dev/null 2>&1; then
    echo "❌ Erro: pip não encontrado no ambiente virtual."
    exit 1
fi

echo "✅ Sucesso: O ambiente virtual está configurado e ativo!"
echo "🐍 Python: $PYTHON_EXEC"
