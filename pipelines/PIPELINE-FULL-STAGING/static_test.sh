#!/bin/bash

source todo-list-aws/bin/activate
set -x

RAD_ERRORS=$(radon cc src -nc | wc -l)

if [[ $RAD_ERRORS -ne 0 ]]; then
    echo 'Ha fallado el análisis estático de RADON - CC'
    exit 1
fi

RAD_ERRORS=$(radon mi src -nc | wc -l)
if [[ $RAD_ERRORS -ne 0 ]]; then
    echo 'Ha fallado el análisis estático de RADON - MI'
    exit 1
fi

flake8 src/*.py
if [[ $? -ne 0 ]]; then
    exit 1
fi

bandit src/*.py
if [[ $? -ne 0 ]]; then
    exit 1
fi

radon cc src -nc  # Agrega esta línea de comando para calcular la complejidad ciclomática

exit 0
