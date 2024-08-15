package main

import (
	"api/structs"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/jmoiron/sqlx"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func OpenConnection() *sqlx.DB {
	err := godotenv.Load()
	if err != nil {
		panic(err)
	}
	user := os.Getenv("user")
	password := os.Getenv("password")
	dbname := os.Getenv("dbname")
	psqlInfo := fmt.Sprintf("user=%s password=%s dbname=%s sslmode=require host=localhost",
		user, password, dbname)
	db, err := sqlx.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}

	err = db.Ping()
	if err != nil {
		panic(err)
	}

	return db
}

func BatterGetHandler(w http.ResponseWriter, r *http.Request) {
	db := OpenConnection()
	defer db.Close()
	var batters []structs.Batter

	err := db.Select(&batters, "SELECT * FROM batting_data")

	if err != nil {
		panic(err)
	}

	batterBytes, _ := json.MarshalIndent(batters, "", "\t")

	w.Header().Set("Content-Type", "application/json")
	w.Write(batterBytes)

}

func PitcherGetHandler(w http.ResponseWriter, r *http.Request) {
	db := OpenConnection()
	defer db.Close()
	var pitchers []structs.Pitcher

	const qstring = "SELECT \"IDfg\",\"Season\",\"Name\",\"Team\",\"Age\",\"W\",\"L\",\"WAR\",\"ERA\",\"G\",\"GS\",\"CG\",\"ShO\",\"SV\",\"BS\",\"IP\",\"TBF\",\"H\",\"R\",\"ER\",\"HR\",\"BB\",\"IBB\",\"HBP\",\"WP\",\"BK\",\"SO\",\"GB\",\"FB\",\"LD\",\"IFFB\",\"Balls\",\"Strikes\",\"Pitches\",\"RS\",\"IFH\",\"BU\",\"BUH\",\"K/9\",\"BB/9\",\"K/BB\",\"H/9\",\"HR/9\",\"AVG\",\"WHIP\",\"BABIP\",\"LOB%\",\"FIP\",\"GB/FB\",\"LD%\",\"GB%\",\"FB%\",\"IFFB%\",\"HR/FB\",\"IFH%\",\"BUH%\",\"Starting\",\"Start-IP\",\"Relieving\",\"Relief-IP\",\"RAR\",\"Dollars\",\"tERA\",\"xFIP\",\"WPA\",\"+WPA\",\"RE24\",\"REW\",\"pLI\",\"inLI\",\"gmLI\",\"exLI\",\"Pulls\",\"WPA/LI\",\"Clutch\",\"FBv\",\"SL%\",\"SLv\",\"CT%\",\"CTv\",\"CB%\",\"CBv\",\"CH%\",\"CHv\",\"SF%\",\"SFv\",\"KN%\",\"KNv\",\"XX%\",\"PO%\",\"wFB\",\"wSL\",\"wCT\",\"wCB\",\"wCH\",\"wSF\",\"wKN\",\"wFB/C\",\"wSL/C\",\"wCT/C\",\"wCB/C\",\"wCH/C\",\"wSF/C\",\"wKN/C\",\"O-Swing%\",\"Z-Swing%\",\"Swing%\",\"O-Contact%\",\"Z-Contact%\",\"Contact%\",\"Zone%\",\"F-Strike%\",\"SwStr%\",\"HLD\",\"SD\",\"MD\",\"ERA-\",\"FIP-\",\"xFIP-\",\"K%\",\"BB%\",\"SIERA\",\"RS/9\",\"E-F\",\"Pace\",\"RA9-WAR\",\"BIP-Wins\",\"LOB-Wins\",\"FDP-Wins\",\"Age Rng\",\"K-BB%\",\"Pull%\",\"Cent%\",\"Oppo%\",\"Soft%\",\"Med%\",\"Hard%\",\"kwERA\",\"TTO%\",\"FRM\",\"K/9+\",\"BB/9+\",\"K/BB+\",\"H/9+\",\"HR/9+\",\"AVG+\",\"WHIP+\",\"BABIP+\",\"LOB%+\",\"K%+\",\"BB%+\",\"LD%+\",\"GB%+\",\"FB%+\",\"HR/FB%+\",\"Pull%+\",\"Cent%+\",\"Oppo%+\",\"Soft%+\",\"Med%+\",\"Hard%+\",\"EV\",\"LA\",\"Barrels\",\"Barrel%\",\"maxEV\",\"HardHit\",\"HardHit%\",\"Events\",\"CStr%\",\"CSW%\",\"xERA\",\"botERA\",\"botOvr\",\"botStf\",\"botCmd\",\"botxRV100\",\"Stuff+\",\"Location+\",\"Pitching+\" FROM pitching_data"

	err := db.Select(&pitchers, qstring)
	if err != nil {
		panic(err)
	}

	pitcherBytes, _ := json.MarshalIndent(pitchers, "", "\t")

	w.Header().Set("Content-Type", "application/json")
	w.Write(pitcherBytes)

}

func main() {
	http.HandleFunc("/bat", BatterGetHandler)
	http.HandleFunc("/pitch", PitcherGetHandler)
	// http.HandleFunc("/insert", POSTHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
