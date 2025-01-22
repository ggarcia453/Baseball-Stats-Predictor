"""
Python Module for adding data to the postgres database.
"""
import os
import argparse
from pybaseball import batting_stats, pitching_stats
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from dotenv import load_dotenv

def main(args: argparse.Namespace):
    #Grab data
    match args.mode:
        case "batting":
            data = batting_stats(args.year)
        case "pitching":
            data = pitching_stats(args.year)
        case _:
            print("not a valid mode")
            return None
    df = pd.DataFrame(data)
    df = df.drop(columns=['IDfg', 'Events'])
    if df.empty:
        print(f"No data found for {args.year}")
        return None

    # Connect to database
    load_dotenv()
    db_name = os.getenv('dbname')
    db_user = os.getenv('user')
    db_password = os.getenv('password')
    db_host = 'localhost'
    db_port = '5432'
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(database_url, echo=False)
    try:

        #Prepare Data 
        df = df.where(pd.notna(df), None)
        records = df.to_dict(orient='records')
        if records:
            with engine.begin() as connection:
                # Insert data with Pandas
                df.to_sql(f"{args.mode}_data", con=engine, if_exists='append', index=False)
                print(f"Successfully inserted {len(records)} rows for {args.year}")
        else:
            print("No records to insert")
    except Exception as e:
        print(e)
    finally:
        engine.dispose()
    return None

if __name__ == "__main__":
    # Parse arguments 
    parser = argparse.ArgumentParser(
        description='Python Module for adding data from pybaseball to database.')
    parser.add_argument('-y', '--year', help="year to retreive")
    parser.add_argument('-m', '--mode', help="mode for data to retrieve")
    args = parser.parse_args()

    main(args)