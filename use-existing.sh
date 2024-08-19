#! /bin/bash
PYTHONSRCPATH=src/main.py
CSV=true
b_p=batting #should be either batting or pitching
start_year=1969
end_year=2019
model_directory=models/AVG-HR-OPS-RAR-wRC+-WAR
name="Barry Bonds"
year=2002
TRAIN=false

if [ ! -d "$model_directory" ]; then
  echo "$model_directory does not exist."
  exit 1
fi

if [ "$TRAIN" = true ] ; then
    python3 $PYTHONSRCPATH -d $b_p"_data_"$start_year"_"$end_year -c -lm $model_directory -rt
else
    python3 $PYTHONSRCPATH -d $b_p"_data_"$start_year"_"$end_year -c -lm $model_directory -pp "$name $year"
fi
