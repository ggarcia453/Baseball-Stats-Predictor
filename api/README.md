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
It returns a json of the folling stats:

### Pitching

The access point for this endpoint is /pitching.
It returns a json of the folling stats:


## Query Parameters
The query parameters for all endpoints are the same. They are listed below. 

Query Parameters:
- team: Filter by team name (use three letter code found in [code table](#code-table))
  - example: Search for Baltimore Orioles PLayers -> ?team=BAL
- name: Filter by player name (use hyphen for spaces)
  - example: "Barry Bonds" -> "Barry-Bonds"
- season: Filter by specific season(s)
  - Single season: ?season=2023 (returns 2023 season alone)
  - Range of seasons: ?season=2020&season=2023 (returns 2020-2023)


## Code Table
This code table is used for filtering stats by specific team. See [Query Parameters](#query-parameters) for more information. 

| Code | Team                          | Division                  |
|------|-------------------------------|---------------------------|
| BAL  | Baltimore Orioles             | AL East                   |
| BOS  | Boston Red Sox                | AL East                   |
| NYY  | New York Yankees              | AL East                   |
| TBR  | Tampa Bay Rays                | AL East                   |
| TOR  | Toronto Blue Jays             | AL East                   |
| CLE  | Cleveland Guardians           | AL Central                |
| DET  | Detroit Tigers                | AL Central                |
| KCR  | Kansas City Royals            | AL Central                |
| MIN  | Minnesota Twins               | AL Central                |
| CHW  | Chicago White Sox             | AL Central                |
| HOU  | Houston Astros                | AL West/NL Central        |
| LAA  | Los Angeles Angels            | AL West                   |
| ANA  | Anaheim Angels                | AL West                   |
| CAL  | California Angels             | AL West                   |
| OAK  | Oakland Athletics             | AL West                   |
| SEA  | Seattle Mariners              | AL West                   |
| TEX  | Texas Rangers                 | AL West                   |
| ATL  | Atlanta Braves                | NL East                   |
| MIA  | Miami Marlins                 | NL East                   |
| NYM  | New York Mets                 | NL East                   |
| PHI  | Philadelphia Phillies         | NL East                   |
| WSN  | Washington Nationals          | NL East                   |
| MON  | Montreal Expos                | NL East                   |
| CHC  | Chicago Cubs                  | NL Central                |
| CIN  | Cincinnati Reds               | NL Central                |
| MIL  | Milwaukee Brewers             | NL Central/AL West        |
| PIT  | Pittsburgh Pirates            | NL Central                |
| STL  | St. Louis Cardinals           | NL Central                |
| ARI  | Arizona Diamondbacks          | NL West                   |
| COL  | Colorado Rockies              | NL West                   |
| LAD  | Los Angeles Dodgers           | NL West                   |
| SDP  | San Diego Padres              | NL West                   |
| SFG  | San Francisco Giants          | NL West                   |
| BEG  | Birmingham Black Barons       | Negro Leagues             |
| BBB  | Baltimore Black Barons        | Negro Leagues             |
| CAG  | Chicago American Giants       | Negro Leagues             |
| CBE  | Cuban Giants                  | Negro Leagues             |
| CBR  | Cuban Stars (West)            | Negro Leagues             |
| CCB  | Cleveland Buckeyes            | Negro Leagues             |
| CC   | Cleveland Cubs                | Negro Leagues             |
| CIC  | Cincinnati Clowns             | Negro Leagues             |
| FLA  | Florida Cuban Giants          | Negro Leagues             |
| HG   | Harrisburg Giants             | Negro Leagues             |
| HSS  | Hilldale Club                 | Negro Leagues             |
| IC   | Indianapolis Clowns           | Negro Leagues             |
| JRC  | Jacksonville Red Caps         | Negro Leagues             |
| KCM  | Kansas City Monarchs          | Negro Leagues             |
| MRS  | Memphis Red Sox               | Negro Leagues             |
| NE   | Newark Eagles                 | Negro Leagues             |
| NBY  | New York Black Yankees        | Negro Leagues             |
| NYC  | New York Cubans               | Negro Leagues             |
| PHA  | Philadelphia Stars            | Negro Leagues             |
| PS   | Pittsburgh Crawfords          | Negro Leagues             |
| SNS  | St. Louis Stars               | Negro Leagues             |
| TIC  | Toledo Crawfords              | Negro Leagues             |
