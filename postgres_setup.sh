#!/bin/bash

USERNAME="USERNAME"
PASSWORD=""

psql -U $USERNAME  -d baseball -a -f batting_data_1945_2023.sql
psql -U $USERNAME  -d baseball -a -f pitching_data_1945_2023.sql
