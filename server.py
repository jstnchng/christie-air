#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://jc4137:christiejustin@w4111a.eastus.cloudapp.azure.com/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#

engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

# cursor = engine.execute("select * from Flights")
# for row in cursor:
#   print list(row)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

@app.route('/search_flights_by_airport', methods=['POST'])
def search_flights_by_airport():
  origin = request.form['origin']
  destination = request.form['destination']

  query = '''
  SELECT F.airline, F.flightnumber, F.origin, F.destination, F.departuretime, F.arrivaltime, F.status 
  FROM Flights F 
  WHERE F.origin = \'''' + origin + '\' AND F.destination = \'' + destination + '\''
  flight_query = g.conn.execute(query)

  flights = []
  for flight in flight_query:
    flights.append( flight )  
  flight_query.close()

  context = dict(flight_data = flights)
  return render_template("search_flights_by_airport.html", **context)

@app.route('/search_flights_by_airline', methods=['POST'])
def search_flights_by_airline():
  airline = request.form['airline']

  query = '''
  SELECT F.airline, F.flightnumber, F.origin, F.destination, F.distance, F.departuretime, F.arrivaltime, F.status 
  FROM Flights F 
  WHERE F.airline = \'''' + airline + '\''
  flight_query = g.conn.execute(query)

  flights = []
  for flight in flight_query:
    flights.append( flight )  
  flight_query.close()

  context = dict(flight_data = flights)
  return render_template("search_flights_by_airline.html", **context)

@app.route('/search_customers_past_flights', methods=['POST'])
def search_customers_past_flights():
  email = request.form['email']
  email_bool = (email != '')

  firstname = request.form['firstname']
  firstname_bool = (firstname != '')

  lastname = request.form['lastname']
  lastname_bool = (lastname != '')

  phonenumber = request.form['phonenumber']
  phonenumber_bool = (phonenumber != '')
  # if(phonenumber_bool):
  #   phonenumber = int(phonenumber)

  query = '''
  SELECT C.firstname, C.middlename, C.lastname, C. birthdate, C.gender, C.phonenumber, F.airline, F.flightnumber, F.origin, F.destination, F.distance, F.departuretime, F.arrivaltime, T.class, T.seat, T.price
  FROM Customers C
  JOIN Tickets T
  ON C.customerid = T.customerid
  JOIN Flights F
  ON F.flightid = T.flightid
  '''

  if( email_bool or firstname_bool or lastname_bool or phonenumber_bool ):
    where_clauses = []
    if(email_bool):
      where_clauses.append('C.email = \'' + email + '\'')
    if(firstname_bool):
      where_clauses.append('C.firstname = \'' + firstname + '\'')
    if(lastname_bool):
      where_clauses.append('C.lastname = \'' + lastname + '\'')
    if(phonenumber_bool):
      where_clauses.append('C.phonenumber = ' + phonenumber)

    query += ' WHERE '
    for i in range(len(where_clauses)-1):
      query += where_clauses[i]
      query += '\n AND '
    query += where_clauses[len(where_clauses)-1]

  flight_query = g.conn.execute(query)

  flights = []
  for flight in flight_query:
    flights.append( flight )  
  flight_query.close()

  context = dict(flight_data = flights)
  return render_template("search_customers_past_flights.html", **context)

@app.route('/find_cheapest_flight', methods=['POST'])
def find_cheapest_flight():
  origin = request.form['origin']
  origin_bool = (origin != '')

  destination = request.form['destination']
  destination_bool = (destination != '')

  airline = request.form['airline']
  airline_bool = (airline != '')

  departure_date = request.form['departure_date']
  departure_date_bool = (departure_date != '')

  arrival_date = request.form['arrival_date']
  arrival_date_bool = (arrival_date != '')

  query = '''
  SELECT T.price, T.class, T.seat, F.airline, F.departureTime, F.arrivalTime, F.origin, F.destination
  FROM Tickets T
  JOIN Flights F
  ON T.flightID = F.flightID
  '''

  if( origin_bool or destination_bool or airline_bool or departure_date_bool or arrival_date_bool):
    where_clauses = []
    if(origin_bool):
      where_clauses.append('F.origin = \'' + origin + '\'')
    if(destination_bool):
      where_clauses.append('F.destination = \'' + destination + '\'')
    if(airline_bool):
      where_clauses.append('F.airline = \'' + airline + '\'')
    if(departure_date_bool):
      where_clauses.append('F.departureTime::date >= date \'' + departure_date + '\'')
    if(arrival_date_bool):
      where_clauses.append('F.arrivalTime::date < date \'' + arrival_date + '\'' + 'interval \'24 hours\'')

    query += ' WHERE '
    for wc in range(len(where_clauses)-1):
      query += wc
      query += '\n AND '
    query += where_clauses[len(where_clauses)-1]

  flight_query = g.conn.execute(query)

  flights = []
  for flight in flight_query:
    flights.append( flight )  
  flight_query.close()

  context = dict(flight_data = flights)
  return render_template("find_cheapest_flight.html", **context)

@app.route('/search_customer_FFA', methods=['POST'])
def search_customer_FFA():
  customer_email = request.form['customer_email']

  query = '''
  SELECT C.firstName, C.lastName, FFA.airline, FFA.mileage
  FROM FrequentFlyerAccounts FFA
  JOIN Customers C
  ON FFA.customerID = C.customerID
  WHERE C.email = \'''' + customer_email + '\''
  flight_query = g.conn.execute(query)

  flights = []
  for flight in flight_query:
    flights.append( flight )  
  flight_query.close()

  context = dict(flight_data = flights)
  return render_template("search_customer_FFA.html", **context)

@app.route('/search_airlines_airplanes', methods=['POST'])
def search_airlines_airplanes():
  airline = request.form['airline']

  query = '''
  SELECT AP.companyname, AP.model, AP.capacity, AL.headquarters
  FROM Airplanes AP
  JOIN Airlines AL
  ON AP.companyname = AL.companyname
  WHERE AP.companyName = \'''' + airline + '\''
  print(query)

  flight_query = g.conn.execute(query)

  flights = []
  for flight in flight_query:
    flights.append( flight )  
  flight_query.close()

  context = dict(flight_data = flights)
  return render_template("search_airlines_airplanes.html", **context)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
