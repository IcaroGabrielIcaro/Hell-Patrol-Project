#!/bin/bash

# Script para executar o cliente Hell Patrol
# Menu com suporte a singleplayer e multiplayer

cd "$(dirname "$0")"

# Ativa ambiente virtual se existir
if [ -d "env" ]; then
    source env/bin/activate
fi

# Executa cliente
python -m client.main
