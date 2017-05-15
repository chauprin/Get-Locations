from flask import Flask, redirect, render_template, request, url_for, flash, jsonify
from models import db
import psycopg2
import random
import timeit

app = Flask(__name__)

#Database configurations of the postgres database
POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_db1',
    'host': 'localhost',
    'port': '5432',
}

#App configurations
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

#Created a cursor for using database
conn = psycopg2.connect(database = 'my_db1', user = 'postgres', password = 'password', host = 'localhost')
curs = conn.cursor()

#Hardcoded latitude and longitude values
latitude = 45.12 
longitude = 71.12

#Home
@app.route('/')
def home():
	return jsonify("Nothing here. Please go to the get, post or register endpoint.")

#Endpoint for generating access parameters for external apps to use this api
@app.route('/register/arguments', methods = ['GET', 'POST'])
def register():
	if request.method == "POST":
		
		#Postgresql gives frequent errors if this commit is not done 
		conn.commit()
		
		application_name = request.args.get("application_name")
		application_website = request.args.get("application_website")

		#Creating a 16 digit random client_id and client_secret 
		client_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16)) 
		client_secret = ''.join(random.choice('0123456789ABCDEF') for i in range(16))

		#Preventing empty field values
		if application_name == "" or application_website == "":
			return jsonify("Empty fields are not allowed")
		
		#The recieved values using register are inserted into clients table
		curs.execute("insert into clients (application_name, application_website, client_id, client_secret) values(%s, %s, %s, %s);",[application_name, application_website, client_id, client_secret])
		conn.commit()

		return jsonify({"Note": "Please note the client_id and client_secret. You will need them for get requests.",
						"Credentials" :	{"application_name" : application_name, 
										"application_website" : application_website,
										"client_id" : client_id,
										"client_secret" : client_secret
							}
						}
					
					)
	else:
		return jsonify("Bad Request. Only post requests are allowed on this endpoint.")

#POST API
@app.route('/post_location/arguments', methods = ['GET','POST'])
def post_location():
	if request.method == "POST":
		conn.commit()
		
		client_id = request.args.get("client_id")
		client_secret = request.args.get("client_secret")
		
		#Fetching client_secret for authentication
		curs.execute("select client_secret from clients where client_id = %s;",[client_id])
		all_results = curs.fetchone()
		
		if client_secret == all_results[0]:
			place = request.args.get("place")
			lat = request.args.get("lat")
			lon = request.args.get("lon")
			
			#Preventing empty fields
			if lat == "" or lon == "" or place == "":
				return jsonify("Empty fields not allowed")	
			
			#The recieved values using post are inserted into my_points table
			curs.execute("insert into my_points (place, lat, lon) values(%s,%s,%s);",[place, lat, lon])
			conn.commit()
			return jsonify("Row Inserted.")
		else:
			return jsonify("Bad Authentication.")
	else:
		return jsonify("Bad request. Only POST requests are allowed on this endpoint.")

#GET_USING_POSTGRES 
@app.route("/get_using_postgres/arguments")
def get_using_postgres():
	client_id = request.args.get("client_id")
	client_secret = request. args.get("client_secret")
	
	#Fetching client_secret for authentication
	curs.execute("select client_secret from clients where client_id = %s;",[client_id])
	all_results = curs.fetchone()
	
	if client_secret == all_results[0]:
		conn.commit()
		
		#Calculating time taken for execution of query for comparison purposes
		start_time = timeit.default_timer()
		curs.execute("select * from my_points where (point(lon,lat) <@> point(%s,%s)) <= 5/1.6;",[longitude,latitude])
		elapsed = timeit.default_timer() - start_time
		
		print "***--- Time taken for get_using_postgres = %s ---***" %(elapsed)
		rows=curs.fetchall()
		return jsonify({"Time taken" : elapsed,
						"results" : rows})
	else:
		return jsonify("Bad Authentication")

#GET_USING_SELF
@app.route("/get_using_self/arguments")
def get_using_self():
	client_id = request.args.get("client_id")
	client_secret = request. args.get("client_secret")
	
	#Fetching client_secret for authentication
	curs.execute("select client_secret from clients where client_id = %s;",[client_id])
	all_results = curs.fetchone()

	if client_secret == all_results[0]:
		conn.commit()
		
		#Calculating execution time for comparison purposes
		start_time = timeit.default_timer()
		curs.execute("select * from ( select s_no, place, lat, lon, (3959 * acos (cos ( radians(%s) ) * cos( radians( lat ) ) * cos( radians( lon ) - radians(%s) ) + sin ( radians(%s) ) * sin( radians( lat ) ) ) ) AS distance FROM my_points order by distance) items where distance < 5/1.6;",[latitude,longitude,latitude])
		elapsed = timeit.default_timer() - start_time
		
		print "***--- Time taken for get_using_self = %s ---***" %(elapsed)
		rows = curs.fetchall()
		return jsonify({"Time taken" : elapsed,
						"results" : rows})
	else:
		return jsonify("Bad Authentication")

if __name__ == '__main__':
    app.run()