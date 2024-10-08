#! /bin/bash
PYTHONSRCPATH=src/main.py
b_p=batting #should be either batting or pitching
model_directory=models/AVG-HR-OPS-RAR-wRC+-WAR
name="Albert Pujols" #Leave Space between first and last name
year=2011
TRAIN=false

if [ ! -d "$model_directory" ]; then
  echo "$model_directory does not exist."
  exit 1
fi

if [ "$TRAIN" = true ] ; then
    python3 $PYTHONSRCPATH -m $b_p -c -lm $model_directory -rt
else
    python3 $PYTHONSRCPATH -m $b_p -c -lm $model_directory -pp "$name $year"
fi
