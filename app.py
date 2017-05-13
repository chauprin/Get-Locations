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

#Cursor for using database
conn = psycopg2.connect(database = 'my_db1', user = 'postgres', password = 'password', host = 'localhost')
curs = conn.cursor()

#Endpoint for generating access parameters for external apps to use this api
@app.route('/', methods = ['GET', 'POST'])
def home():
	if request.method == "POST":
		conn.commit()
		name = request.form['name']
		email = request.form['email']
		client_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
		client_secret = ''.join(random.choice('0123456789ABCDEF') for i in range(16))    	
		if name == "" or email == "":
			return render_template("home.html", error = "Empty fields not allowed")
		curs.execute("insert into clients (name, email, client_id, client_secret) values(%s, %s, %s, %s);",[name, email, client_id, client_secret])
		conn.commit()
		message = "Your CLIENT_ID = %s and your CLIENT_SECRET = %s. Please note these. You are gonna need them for using this api" %(client_id, client_secret)
		return render_template('home.html', message = message)
	else:
		return render_template("home.html")

#POST API, No authorization required to post
@app.route('/post_location', methods = ['GET','POST'])
def post_location():
	if request.method == "POST":
		conn.commit()
		place = request.form['place']
		lat = request.form['lat']
		lon = request.form['lon']
		if lat == "" or lon == "" or place == "":
			return render_template("index.html", error = "Empty fields not allowed")	
		curs.execute("insert into my_points (place, lat, lon) values(%s,%s,%s);",[place, lat, lon])
		conn.commit()
		return redirect(url_for('post_location'))
	else:
		return render_template("index.html")

#GET_USING_POSTGRES API
@app.route("/get_using_postgres/auth")
def get_using_postgres():
	client_id = request.args.get("client_id")
	client_secret = request. args.get("client_secret")
	curs.execute("select client_secret from clients where client_id = %s;",[client_id])
	all_results = curs.fetchone()
	if client_secret == all_results[0]:
		conn.commit()
		latitude = 30.31
		longitude = 78.03
		start_time = timeit.default_timer()
		curs.execute("select * from my_points where (point(lon,lat) <@> point(%s,%s)) <= 5/1.6;",[longitude,latitude])
		elapsed = timeit.default_timer() - start_time
		print "***--- Time taken for get_using_postgres = %s ---***" %(elapsed)
		rows=curs.fetchall()
		return jsonify(rows)
	else:
		return jsonify("Bad Authentication")

#GET_USING_SELF
@app.route("/get_using_self/auth")
def get_using_self():
	client_id = request.args.get("client_id")
	client_secret = request. args.get("client_secret")
	curs.execute("select client_secret from clients where client_id = %s;",[client_id])
	all_results = curs.fetchone()
	
	if client_secret == all_results[0]:
		conn.commit()
		latitude = 30.31
		longitude = 78.03
		start_time = timeit.default_timer()
		curs.execute("select * from ( select s_no, place, lat, lon, (3959 * acos (cos ( radians(%s) ) * cos( radians( lat ) ) * cos( radians( lon ) - radians(%s) ) + sin ( radians(%s) ) * sin( radians( lat ) ) ) ) AS distance FROM my_points order by distance) items where distance < 5/1.6;",[latitude,longitude,latitude])
		elapsed = timeit.default_timer() - start_time
		print "***--- Time taken for get_using_self = %s ---***" %(elapsed)
		rows = curs.fetchall()
		return jsonify(rows)
	else:
		return jsonify("Bad Authentication")

if __name__ == '__main__':
    app.run()