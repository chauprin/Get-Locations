# Get-Locations
A REST API to get nearby points to a particular latitude longitude using extensions of postgres and without them also.    
    
Includes authentication using grant type = client credentials     
Implemented using Python, Flask, PostgreSQL and data migration     
     
Usage :      
Make sure you have PostgreSQL and its extensions postgis, cube, earthdistance installed and created database "my_db1" using "CREATE DATABASE my_db1;" in psql terminal       
Browse to the project directory in terminal and run the following commands for data migrations if not already done :         
1. python manage.py db init      
2. python manage.py db migrate      
3. python manage.py db upgrade      
     
Now run the app using "python app.py"     
     
There are four endpoints    
1. Register : for other apps to register and get Client Credentials to use this API    
http://localhost:5000/register/arguments?application_name=APPLICATION_NAME&application_website=APPLICATION_WEBSITE    
2. Post Location : The clients can post data about location using this endpoint by using the Client   Credentials    
http://localhost:5000/post_location/arguments?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&place=PLACE_NAME&lat=LATITUDE&lon=LONGITUDE    
3. Get Using Postgres : Gives places inside 5 km of the hardcoded latitude and longitude values by using extensions of PostgreSQL    
http://localhost:5000/get_using_postgres/arguments?client_id=CLIENT_ID&client_secret=CLIENT_SECRET    
4. Get Using Self : Also gives places inside 5 km of the hardcoded latitude and longitude values by mathematical calculations     
http://localhost:5000/get_using_self/arguments?client_id=CLIENT_ID&client_secret=CLIENT_SECRET 


