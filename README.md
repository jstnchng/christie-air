# w4111-proj
README

************************************************************************************************************************

Christie Ho cch2164
Justin Chang jc4137

************************************************************************************************************************

* PostgreSQL Account *

	username: jc4137
	password: christiejustin
	database:w4111a.eastus.cloudapp.azure.com/proj1part2

************************************************************************************************************************

* URL of Web Application *

	http://40.76.37.130:8111

************************************************************************************************************************

* Description *

	The parts of our original proposal that we implemented:
		The user can search for:
			- flights going out of and going to a particular airport
			- flights from a particular airline
			- past ticket records for a customer given email/ first name/ last name/ phone number/ flight number
			- flight prices given origin/ destination/ airline/ departure date/ arrival date (all fields are optional)
			- status of a flight and departure times/ arriving times given flight number
	The parts of our original proposal not implemented:
		We didn’t have functionality to find the gate a flight leaves out of, because our schema changed to no longer include gate. 
		We also didn’t have functionality to book a flight because we built our website to provide information instead of serve as a booking website.
	The parts not from our original proposal that we implemented:
		- find frequent flyer account information for a customer given customer email
		- search all airplanes owned by a particular airline

************************************************************************************************************************

* Most Interesting Pages *

Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

	The following functionalities render the most interesting database operations: find flight prices given any of hte fields and find customer's past flight information. 

		- Flight Prices

			In displaying flight prices, we display a table with tickets of flights ordered by their price that satisfy a particular origin and destination as well as airline, departure date, or arrival date as described by the user. It will help facilitate a user trying to find the cheapest tickets for a particular flight from an origin to the destination with any other specified information. 

			To find flight prices, the only required fields the user inputs are the origin and destination because otherwise the flight information rendered is useless to the average consume. We assume that the average consumer knows where he/she wants to go. The airline field, departure date field, and arrival date field are optional as to not constrain the user to a particular airline or a particular departure or arrival date.

			This query is interesting because it requires a join clause of both the tickets and flights table, an order by clause for the ticket's prices, and a variable number of where clauses depending on which fields the user selects to input. Each field that is entered from the home page contributes to the where clause conditions. This query is also interesting because it is a very applicable in the real world in that a consumer would really be interested in finding out ticket prices for particular flights out of a particular origin to a particular destination. 

		- Customer's Past Flight Information

			In displaying customer's past flight information, we display a table with all the tickets of flights that a customer with the matching information has taken. It will help users get the information about the customer, all the flights that a particular individual has taken, and the ticket information. 

			To find a customer's past flight information, there are no required fields, meaning a consumer can get all the past flight information of all the customer's in our database. The first name, last name, email, phone number, and flight number are all optionl fields. Any user can input a subset of them, whatever best matches the information that they know. This helps in not forcing the consumer to know about all the neceesaary information of a customer before being able to search all the potential past flights. 

			This query is interesting because it requires two join clauses of the tickets, flights, and customers tables as well as a variable number of where clauses depending on which fileds the user selects to input. Each field that is entered from the home page contributes to the where clause conditions. In addition, this query is interesting because it contains a lot of information, so it is necessary to figure out which information we would like to keep and which we would like to display. 


