# Modelling Calendar Data

### To run the application
* Run main.py and open http://127.0.0.1:5000 on the browser
* From the application we can do,
  - Uploading the ics type file
  - Add an event
  - validate the event
  - List the upcoming events on a given date
  - List the upcoming events happening in Saint-Etienne that are not courses
  - Add an attendee 

### To see graph on web
* Run graph_on_web.py and open http://127.0.0.1:5000/caldata on the browser

### Queries
* To post all our events in the graph to the container run post_events_to_ldp.py
* To get all the events related to our graph run get_all_events.py
* To get upcoming events run get_upcomingevents.py
* To get events happening in Saint-Etienne that are not courses run get_particularEvent.py
* To post a new event to the container run post_newEvent.py, It will generate a unique id(uid) for every event.
* To delete a particular event in the container run delete_oneEvent.py
* To add an attendee to the event to represent the person attended the event run add_attendeee_toEvent.py
* To validate our graph with SHACL run validateshacl.py

[Note]: We will write a report to explaining our works, functionalities, queries etc and we will submit it by before 20th january


### Main Objectives
* Design a Calendar  
  - It should be available online
  - It should be represented in a standard vocabulary
* Develop an Application to :
  * Create calender events
  * Query calender events
  * Validate calender events

### Territoire LDP
* Create a LDP container at https://www.w3.org/TR/ldp/#ldpc

### Technical Requirements 
* R1 - Application must download any ICS file and turn it into RDF
  * [Note]: Use identifiers from Plateforme Territoire's LDP to denote rooms
* R2 - Add events to personal calender hosted on Platforme Territoire's LDP
  * [Note]: Events can generated from ICS file, extracted from Web pages or manually written
* R3 - List of upcoming events on a given date
  * [Node]: This feature should include at least one SPARQL query
* R4 - List events taking place in Saint-Etienne that are not courses
  * [Note]: use SPARQL
* R5 - Modify an existing event to indicate that someone has attended it
  * [Note]: (e.g. "I attended the last SemWeb lecture").
  * How to do : GET event id from the user and send a post request back to the ldp
* R6 - Validate the information defined for a given event.
  * [Note]: use SHACL
* R7 - Validate the information defined for CPS2 course
  * [Note]: it should either be organized by UJM or EMSE and be held in one of the university locations of Saint-Étienne
* R8 - Discover other resources and link a resource describing an event to another resource describing the same event
  * [Note]: The property used for linking should be owl:sameAs
* R9 - Take owl:sameAs statements into account when answering SPARQL queries: if two resources are declared to be the same, they must both be part of an answer.


