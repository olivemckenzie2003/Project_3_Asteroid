#########################################################################
##                                                                     ##
##   0. Imports                                                        ##
##                                                                     ##
#########################################################################

# 0.1 Import Flask, jsonify and render_template
from flask import Flask, jsonify, render_template, send_from_directory


# 0.3 Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
# make sure to create config file in vscode
from config1 import password


#########################################################################
##                                                                     ##
##   3. Starting DB
##                                                                     ##
#########################################################################


# connect to local database
protocol = 'postgresql'
username = 'postgres'
host = 'localhost'
port = 5432               
database_name = 'Project_3_Asteriods'
rds_connection_string = f'{protocol}://{username}:{password}@{host}:{port}/{database_name}'
engine = create_engine(rds_connection_string)

# 10.1 Set app name as "app" and start Flask
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/asteroids_v1")
def asteroids_v1():
    session = Session(bind=engine)
    execute_string = "select * from asteriod_df"
    asteriod_data = engine.execute(execute_string).fetchall()
    session.close()
    print("Hi!")

    asteroid_lst = []
    for row in asteriod_data:
        asteroid_lst.append({"id": row[0],
                             "name": row[1],
                             "magnitude": float(row[2]),
                             "hazardous": row[3],
                             "km_min": float(row[4]),
                             "km_max": float(row[5]),
                             "ft_min": float(row[6]),
                             "ft_max": float(row[7]),
                             "velocity_kph": float(row[8]),
                             "velocity_mph": float(row[9]),
                             "miss_distance_km": float(row[10]),
                             "miss_distance_miles": float(row[11])})

    return(jsonify(asteroid_lst))

@app.route("/api/asteroids_v2")
def asteroids_v2():
    session = Session(bind=engine)
    execute_string = "select * from pot_hazardous"
    asteriod_data = engine.execute(execute_string).fetchall()
    session.close()
    print("Hi!")

    hazardous_lst = []
    for row in asteriod_data:
        hazardous_lst.append({"hazardous": row[0],
                             "count": row[1]})

    return(jsonify(hazardous_lst))


if __name__ == '__main__':
    app.run(debug=True)
