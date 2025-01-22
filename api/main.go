package main

import (
	"api/structs"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"slices"
	"sort"
	"strings"

	"github.com/jmoiron/sqlx"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func qstringBuilder(startingString string, values url.Values) string {
	if len(values) == 0 {
		return startingString + " LIMIT 2;"
	}
	textCategories := []string{"team", "name"}

	keys := make([]string, 0, len(values))
	for k := range values {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	conditions := make([]string, 0, len(values))
	for _, k := range keys {
		v := values[k]
		comparator := strings.ToLower(k)
		if slices.Contains(textCategories, comparator) {
			condition := fmt.Sprintf("\"%s\" LIKE '%s'",
				k,
				strings.Join(strings.Split(v[0], "-"), " "))
			conditions = append(conditions, condition)
		} else {
			if len(v) > 1 {
				firstYear := slices.Min(v)
				lastYear := slices.Max(v)
				condition := fmt.Sprintf("\"%s\" >= %s AND \"%s\" <= %s",
					k, firstYear, k, lastYear)
				conditions = append(conditions, condition)
			} else {
				condition := fmt.Sprintf("\"%s\" = %s", k, v[0])
				conditions = append(conditions, condition)
			}
		}
	}
	return startingString + " WHERE " + strings.Join(conditions, " AND ") + ";"
}

func OpenConnection() (*sqlx.DB, error) {
	err := godotenv.Load()
	if err != nil {
		return nil, fmt.Errorf("error loading environment variables: %w", err)
	}
	user := os.Getenv("user")
	password := os.Getenv("password")
	dbname := os.Getenv("dbname")
	psqlInfo := fmt.Sprintf("user=%s password=%s dbname=%s sslmode=require host=localhost",
		user, password, dbname)
	db, err := sqlx.Open("postgres", psqlInfo)
	if err != nil {
		return nil, fmt.Errorf("error opening DB connection: %w", err)
	}

	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("error pinging DB: %w", err)
	}

	return db, nil
}

func BatterGetHandler(w http.ResponseWriter, r *http.Request) {
	db, err := OpenConnection()
	if err != nil {
		panic(err)
	}
	defer db.Close()
	var batters []structs.Batter
	var qstring = "SELECT \"Season\", \"Name\", \"Team\", \"Age\", \"G\", \"AB\", \"PA\", \"H\", \"1B\", \"2B\", \"3B\", \"HR\", \"R\", \"RBI\", \"BB\", \"IBB\", \"SO\", \"HBP\", \"SF\", \"SH\", \"GDP\", \"SB\", \"CS\", \"AVG\", \"GB\", \"FB\", \"LD\", \"IFFB\", \"Pitches\", \"Balls\", \"Strikes\", \"IFH\", \"BU\", \"BUH\", \"BB%\", \"K%\", \"BB/K\", \"OBP\", \"SLG\", \"OPS\", \"ISO\", \"BABIP\", \"GB/FB\", \"LD%\", \"GB%\", \"FB%\", \"IFFB%\", \"HR/FB\", \"IFH%\", \"BUH%\", \"wOBA\", \"wRAA\", \"wRC\", \"Bat\", \"Fld\", \"Rep\", \"Pos\", \"RAR\", \"WAR\", \"Dol\", \"Spd\", \"wRC+\", \"WPA\", \"RE24\", \"REW\", \"pLI\", \"phLI\", \"WPA/LI\", \"Clutch\", \"EV\", \"LA\", \"Barrels\", \"Barrel%\", \"maxEV\", \"HardHit\", \"HardHit%\", \"CStr%\", \"CSW%\", \"xBA\", \"xSLG\", \"xwOBA\" FROM batting_data"
	values := r.URL.Query()
	qstring = qstringBuilder(qstring, values)
	err = db.Select(&batters, qstring)

	if err != nil {
		panic(err)
	}

	batterBytes, _ := json.MarshalIndent(batters, "", "\t")

	w.Header().Set("Content-Type", "application/json")
	w.Write(batterBytes)

}

func PitcherGetHandler(w http.ResponseWriter, r *http.Request) {
	db, err := OpenConnection()
	if err != nil {
		panic(err)
	}
	defer db.Close()
	var pitchers []structs.Pitcher

	var qstring = "SELECT \"Season\",\"Name\",\"Team\",\"Age\",\"W\",\"L\",\"WAR\",\"ERA\",\"G\",\"GS\",\"CG\",\"ShO\",\"SV\",\"BS\",\"IP\",\"TBF\",\"H\",\"R\",\"ER\",\"HR\",\"BB\",\"IBB\",\"HBP\",\"WP\",\"BK\",\"SO\",\"GB\",\"FB\",\"LD\",\"IFFB\",\"Balls\",\"Strikes\",\"Pitches\",\"RS\",\"IFH\",\"BU\",\"BUH\",\"K/9\",\"BB/9\",\"K/BB\",\"H/9\",\"HR/9\",\"AVG\",\"WHIP\",\"BABIP\",\"LOB%\",\"FIP\",\"GB/FB\",\"LD%\",\"GB%\",\"FB%\",\"IFFB%\",\"HR/FB\",\"IFH%\",\"BUH%\",\"Starting\",\"Start-IP\",\"Relieving\",\"Relief-IP\",\"RAR\",\"Dollars\",\"tERA\",\"xFIP\",\"WPA\",\"+WPA\",\"RE24\",\"REW\",\"pLI\",\"inLI\",\"gmLI\",\"exLI\",\"Pulls\",\"WPA/LI\",\"Clutch\",\"FBv\",\"SL%\",\"SLv\",\"CT%\",\"CTv\",\"CB%\",\"CBv\",\"CH%\",\"CHv\",\"SF%\",\"SFv\",\"KN%\",\"KNv\",\"XX%\",\"PO%\",\"wFB\",\"wSL\",\"wCT\",\"wCB\",\"wCH\",\"wSF\",\"wKN\",\"wFB/C\",\"wSL/C\",\"wCT/C\",\"wCB/C\",\"wCH/C\",\"wSF/C\",\"wKN/C\",\"O-Swing%\",\"Z-Swing%\",\"Swing%\",\"O-Contact%\",\"Z-Contact%\",\"Contact%\",\"Zone%\",\"F-Strike%\",\"SwStr%\",\"HLD\",\"SD\",\"MD\",\"ERA-\",\"FIP-\",\"xFIP-\",\"K%\",\"BB%\",\"SIERA\",\"RS/9\",\"E-F\",\"Pace\",\"RA9-WAR\",\"BIP-Wins\",\"LOB-Wins\",\"FDP-Wins\",\"Age Rng\",\"K-BB%\",\"Pull%\",\"Cent%\",\"Oppo%\",\"Soft%\",\"Med%\",\"Hard%\",\"kwERA\",\"TTO%\",\"FRM\",\"K/9+\",\"BB/9+\",\"K/BB+\",\"H/9+\",\"HR/9+\",\"AVG+\",\"WHIP+\",\"BABIP+\",\"LOB%+\",\"K%+\",\"BB%+\",\"LD%+\",\"GB%+\",\"FB%+\",\"HR/FB%+\",\"Pull%+\",\"Cent%+\",\"Oppo%+\",\"Soft%+\",\"Med%+\",\"Hard%+\",\"EV\",\"LA\",\"Barrels\",\"Barrel%\",\"maxEV\",\"HardHit\",\"HardHit%\",\"Events\",\"CStr%\",\"CSW%\",\"xERA\",\"botERA\",\"botOvr\",\"botStf\",\"botCmd\",\"botxRV100\",\"Stuff+\",\"Location+\",\"Pitching+\" FROM pitching_data"
	values := r.URL.Query()
	qstring = qstringBuilder(qstring, values)

	err = db.Select(&pitchers, qstring)
	if err != nil {
		panic(err)
	}

	pitcherBytes, _ := json.MarshalIndent(pitchers, "", "\t")

	w.Header().Set("Content-Type", "application/json")
	w.Write(pitcherBytes)

}

func main() {
	http.HandleFunc("/batting", BatterGetHandler)
	http.HandleFunc("/pitching", PitcherGetHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
