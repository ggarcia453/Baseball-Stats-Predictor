#! /bin/bash
PYTHONSRCPATH=src/main.py
CSV=true
EPOCH_NUM=250


if [ "$CSV" = true ] ; then
    python3 $PYTHONSRCPATH -c -i wRC+ -e $EPOCH_NUM
else
    python3 $PYTHONSRCPATH -i OPS -e $EPOCH_NUM
fi
