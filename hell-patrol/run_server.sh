#!/bin/bash

# Script para executar servidor Hell Patrol
# Servidor dedicado para hospedar partidas

cd "$(dirname "$0")"

# Ativa ambiente virtual se existir
if [ -d "env" ]; then
    source env/bin/activate
fi

# Executa servidor
python -m server.main
