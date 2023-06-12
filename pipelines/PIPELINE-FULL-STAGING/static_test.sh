#!/bin/bash

source todo-list-aws/bin/activate
set -x

RAD_ERRORS=$(radon cc src -nc | wc -l)

if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - CC'
    exit 1
fi
RAD_ERRORS=$(radon mi src -nc | wc -l)
if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - MI'
    exit 1
fi

flake8 src/*.py
if [[ $? -ne 0 ]]
then
    exit 1
fi
bandit src/*.py
if [[ $? -ne 0 ]]
then
    exit 1
fi
##Calculo de la complejidad ciclomatica del codigo.
CC=$(radon cc -a src | awk '{sum+=$2}END{print sum/NR}')

if (( $(echo "$CC <= 5" | bc -l) )); then
    echo "Calidad del código: A"
elif (( $(echo "$CC <= 10" | bc -l) )); then
    echo "Calidad del código: B"
elif (( $(echo "$CC <= 15" | bc -l) )); then
    echo "Calidad del código: C"
elif (( $(echo "$CC <= 20" | bc -l) )); then
    echo "Calidad del código: D"
elif (( $(echo "$CC <= 25" | bc -l) )); then
    echo "Calidad del código: E"
else
    echo "Calidad del código: F"
fi


exit 0
