#! /bin/bash
PYTHONSRCPATH=src/main.py
b_p=batting #should be either batting or pitching
model_directory=models/AVG-BABIP-G-HR-K%-RAR-wRC+-WAR
## For prediction purposes
name="Albert Pujols" #Leave Space between first and last name
year=2017

if [ ! -d "$model_directory" ]; then
  echo "$model_directory does not exist."
  exit 1
fi

if ! nc -z localhost 8080 &>/dev/null; then
    cd api && go run . &
    pid1=$!
    python3 $PYTHONSRCPATH -m $b_p -lm $model_directory -pp "$name $year"& 
    pid2=$!
    wait -n $pid1 $pid2
    kill $pid1 $pid2 2>/dev/null
else
    python3 $PYTHONSRCPATH -m $b_p -lm $model_directory -pp "$name $year"
fi 
