# Overview
A REST API for accessing baseball statistics for both batters and pitchers. The API provides access to extensive statistical data including traditional stats, advanced metrics, and detailed pitch information.

# Structure

- batting_data.sql/pitching_data.sql: Sql files to setup Tables for api use. 
- main.go: Main Go Driver File for API. 
- structs/: Folder with go declarations for structs for pitcher and batter stats. 
- .env: Environment variables
    - USERNAME - Postgres username
    - PASSWORD - Postgres password
    - DATABASE - SQL Database that holds related tables. 

# Setup

## Necessary Components
You will need the following software installed:
- PostgreSQL
- Go 

You will also have to include a .env file with the variables as described in structure. 

## Steps to use
1. Run the SQL setup files to create the required tables
2. Install Go dependencies:
```bash 
go get github.com/jmoiron/sqlx
go get github.com/joho/godotenv
go get github.com/lib/pq
```

3. To run server you can use 
```bash
go run main.go
go run . 
``` 
# Use
This section details how to use the API and what can be expected when running the code. 

## Endpoints

### Batting 

The access point for this endpoint is /batting. 
The query parameters are as folows:
- team: Filter by team name ()
- name: Filter by player name (use hyphen for spaces)
- season: Filter by specific season(s)
    - Single season: ?season=2023
    - Range of seasons: ?season=2020&season=2023 (returns 2020-2023)

### Pitching

The query parameters are as follows:

Query Parameters:
- team: Filter by team name ()
- name: Filter by player name (use hyphen for spaces)
- season: Filter by specific season(s)
  - Single season: ?season=2023
  - Range of seasons: ?season=2020&season=2023 (returns 2020-2023)


## Code Table
