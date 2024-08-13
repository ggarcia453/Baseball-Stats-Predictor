#!/bin/bash

USERNAME="USERNAME"
PASSWORD=""

psql -U $USERNAME  -d baseball -a -f api/batting_data.sql
# psql -U $USERNAME  -d baseball -a -f api/pitching_data_1945_2023.sql
