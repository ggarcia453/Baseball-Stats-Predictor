#! /bin/bash
PYTHONSRCPATH=src/main.py
b_p=batting #should be either batting or pitching
model_directory=models/AVG-HR-OPS-RAR-wRC+-WAR
EVAL=false
## For evaluation purposes
b_p=batting #should be either batting or pitching
start_year=1940
end_year=2023
## For prediction purposes
name="Albert Pujols" #Leave Space between first and last name
year=2004

if [ ! -d "$model_directory" ]; then
  echo "$model_directory does not exist."
  exit 1
fi

if [ "$EVAL" = true ] ; then
    python3 $PYTHONSRCPATH -m $b_p -c -lm $model_directory -ev -m  $b_p -y $start_year"_"$end_year -ple
else
    cd api && go run . &
    pid1=$!
    python3 $PYTHONSRCPATH -m $b_p -c -lm $model_directory -pp "$name $year"& 
    pid2=$!
    wait -n $pid1 $pid2
    kill $pid1 $pid2 2>/dev/null

fi
