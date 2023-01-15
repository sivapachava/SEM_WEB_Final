import os
import uuid
import requests
from flask import Flask, render_template, request, flash, redirect
from SPARQLWrapper import SPARQLWrapper, JSON
from icalendar import Calendar
from rdflib import Graph, Namespace, Literal, URIRef, XSD
from werkzeug.utils import secure_filename
from pyshacl import validate

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'ttl', 'ics'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

container = 'https://territoire.emse.fr/ldp/spsk/'
username = "ldpuser"
password = "LinkedDataIsGreat"
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = Namespace("https://schema.org/")
ldp = Namespace("http://www.w3.org/ns/ldp#")
sparql = SPARQLWrapper('https://territoire.emse.fr/ldp/')
sparql.setReturnFormat(JSON)
sparql.setCredentials("ldpuser", "LinkedDataIsGreat")

@app.route('/')
def hello():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
       if 'file' not in request.files:
           flash('No file part')
           return redirect(request.url)

       file = request.files['file']

       if file.filename == '':
           flash('No selected file')
           return redirect(request.url)

       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           #return redirect(url_for('upload_file', name=filename))


           file = "static/uploads/" + file.filename
           print(file)
           g = Graph()
           g.bind("rdf", rdf)
           g.bind("rdfs", rdfs)
           g.bind("schema", SCHEMA)
           g.bind("ldp", ldp)

           my_container = URIRef("https://territoire.emse.fr/ldp/spsk/")

           g.add((my_container, rdf.type, SCHEMA.Thing))
           g.add((my_container, rdf.type, SCHEMA.schedule))
           g.add((my_container, SCHEMA.description,
                  Literal("The graph contains the representation of our university Calender events", lang=("en"))))

           with open(file, 'r') as f:
               print("Opened File:", file)
               ecal = Calendar.from_ical(f.read())
               for component in ecal.walk():
                   print("Looping through each event")
                   if component.name == "VEVENT":
                       description = component.decoded("DESCRIPTION").decode("utf-8").split()
                       description = description[:-3]
                       wdescription = ' '.join(description)
                       uid = component.get("uid")
                       url = "/{}".format(uid)
                       schedule = URIRef(url)

                       dtstart = str(component.decoded("dtstart")).split()
                       dtstartdate = dtstart[0]
                       # print(dtstartdate)
                       dtstarttime = dtstart[1]
                       # print(dtstarttime)

                       dtend = str(component.decoded("dtend")).split()
                       dtenddate = dtend[0]
                       # print(dtenddate)
                       dtendtime = dtend[1]
                       # print(dtendtime)

                       g.add((my_container, ldp.containes, schedule))
                       g.add((schedule, rdf.type, SCHEMA.Event))
                       g.add((schedule, SCHEMA.name, Literal(component.get("summary"), datatype=XSD.string)))
                       g.add((schedule, SCHEMA.location, Literal(component.get("location"), datatype=XSD.string)))
                       g.add((schedule, SCHEMA.startDate, Literal(dtstartdate, datatype=XSD.date)))
                       g.add((schedule, SCHEMA.startTime, Literal(dtstarttime, datatype=XSD.time)))
                       g.add((schedule, SCHEMA.endDate, Literal(dtenddate, datatype=XSD.date)))
                       g.add((schedule, SCHEMA.endTime, Literal(dtendtime, datatype=XSD.time)))
                       g.add((schedule, SCHEMA.organizer, Literal(wdescription)))
                       g.add((schedule, SCHEMA.uid, Literal(component.get("uid"))))

               f.close()
           print("File closed")
           print(g.serialize(r"rdf_calender.ttl", format="ttl"))

           g = Graph().parse("rdf_calender.ttl")
           g.bind("rdf", rdf)
           g.bind("rdfs", rdfs)
           g.bind("schema", SCHEMA)
           g.bind("ldp", ldp)
           graph_name = 'rdf_calender.ttl'
           for event in g.subjects(rdf.type, SCHEMA.Event):
               print(event)

               startDate = g.value(event, SCHEMA.startDate)
               startTime = g.value(event, SCHEMA.startTime)
               endDate = g.value(event, SCHEMA.endDate)
               endTime = g.value(event, SCHEMA.endTime)
               location = g.value(event, SCHEMA.location)
               director = g.value(event, SCHEMA.organizer)
               # print(director)
               uid = g.value(event, SCHEMA.uid)
               # print(uid)
               name = g.value(event, SCHEMA.name)

               schedule_url = "/{}".format(uid)
               schedule = URIRef(schedule_url)

               graph = Graph()
               # graph.add((schedule, ldp.containes, event))
               graph.add((schedule, rdf.type, SCHEMA.Event))
               graph.add((schedule, SCHEMA.uid, Literal(uid)))
               graph.add((schedule, SCHEMA.startDate, Literal(startDate, datatype=XSD.date)))
               graph.add((schedule, SCHEMA.startTime, Literal(startTime, datatype=XSD.time)))
               graph.add((schedule, SCHEMA.endDate, Literal(endDate, datatype=XSD.date)))
               graph.add((schedule, SCHEMA.endTime, Literal(endTime, datatype=XSD.time)))
               graph.add((schedule, SCHEMA.location, Literal(location, )))
               graph.add((schedule, SCHEMA.organizer, Literal(director, datatype=XSD.string)))
               graph.add((schedule, SCHEMA.name, Literal(name)))

               headers = {
                   'Content-type': 'text/turtle'
               }

               event = graph.serialize()

               params = {'graph': graph_name}
               response = requests.post(container, headers=headers, auth=(username, password), params=params,
                                        data=event)

               sparql.setQuery(f"""
                       PREFIX ldp: <http://www.w3.org/ns/ldp#>
                       PREFIX ns0: <https://carbonldp.com/ns/v1/platform#> 
                       PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
                       PREFIX ns1: <https://schema.org/>

                       SELECT ?id
                       WHERE {{
                           "{container}" ldp:hasMemberRelation ldp:member ;
                           ldp:member ?id.

                       }}
                       LIMIT 10
                       """
                               )
               try:
                   qres = sparql.queryAndConvert()

                   for r in qres["results"]["bindings"]:
                       print(r["id"]["value"])
               except Exception as e:
                   print(e)
           return qres
    return '''
            <!doctype html>
            <title>File uploaded</title>
            '''

#AddEvent
@app.route('/add_event', methods=['POST'])
def add_event():
        ## Extract data from the form to add to the event graph
        form_data = request.form
        name = request.form.get("eventName")
        startDate = request.form.get("startDate")
        startTime = request.form.get("startTime")
        endDate = request.form.get("endDate")
        endTime = request.form.get("endTime")
        location = request.form.get("locationName")
        organizer = request.form.get("organizerName")

        ## Create an Event graph to upload to the Linked Data platform
        container = 'https://territoire.emse.fr/ldp/spsk/'
        username = "ldpuser"
        password = "LinkedDataIsGreat"

        rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
        SCHEMA = Namespace("https://schema.org/")

        graph= Graph()
        graph.bind("rdf", rdf)
        graph.bind("rdfs", rdfs)
        graph.bind("schema", SCHEMA)
        uid = uuid.uuid4()
        uid = "ade" + str(uid)
        print(uid)
        schedule_url = "/{}".format(uid)
        schedule = URIRef( schedule_url )

        graph.add((schedule, rdf.type, SCHEMA.Event))
        graph.add((schedule, SCHEMA.startDate, Literal(startDate, datatype = XSD.date)))
        graph.add((schedule, SCHEMA.startTime, Literal(startTime, datatype = XSD.time)))
        graph.add((schedule, SCHEMA.endDate, Literal(endDate, datatype = XSD.date)))
        graph.add((schedule, SCHEMA.endTime, Literal(endTime, datatype = XSD.time)))
        graph.add((schedule, SCHEMA.location, Literal(location)))   
        graph.add((schedule, SCHEMA.organizer, Literal(organizer, datatype = XSD.string)))    
        graph.add((schedule, SCHEMA.name, Literal(name, datatype = XSD.string)))    
            
        headers = {
                'Content-type': 'text/turtle'
            }
        event= graph.serialize()

        shape_graph = "EVENT_F.ttl" ##SHACL shape for validating an Event
        data_graph = event
        r = validate(data_graph,
                     shacl_graph=shape_graph,
                     inference='rdfs',
                     debug=False,
                     report_graph="ttl"
                     )
        conforms, report_graph, results_text = r
        if conforms:
            requests.post(container, headers=headers,  auth=(username, password), data=event)
            response = "Validation is: "+ str(conforms) + ". The events are uploaded to the Linked Data Platform at : " + str(container)+ str(uid)
            return response
        elif not conforms:
            return "Validation failed due to "+ results_text

#R3 - ListUpcomingEvents
@app.route('/upcoming_events', methods=['GET'])
def upcoming_events():
    form_data = request.form
    eventDate = request.args.get("eventdate")
    print(eventDate)
    sparql.setQuery(f"""
        PREFIX ldp: <http://www.w3.org/ns/ldp#>
        PREFIX ns0: <https://carbonldp.com/ns/v1/platform#> 
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
        PREFIX ns1: <https://schema.org/>

        SELECT ?id
        WHERE {{
            <https://territoire.emse.fr/ldp/spsk/> ldp:hasMemberRelation ldp:member ;
            ldp:member ?id.
            ?id ns1:startDate "{eventDate}"^^xsd:date.

        }}
        LIMIT 10
        """
                    )

    try:
        qres = sparql.queryAndConvert()

        for r in qres["results"]["bindings"]:
            print(r)
    except Exception as e:
        print(e)

    return qres

#R4 - ListEventsThatAreNotCourses(requires a property to define the type of a event)
@app.route('/list_other_events', methods=['GET'])
def list_other_events():
    dateEvent = request.args.get("dateEvent")
    print(dateEvent)
    sparql.setQuery(f"""
        PREFIX ldp: <http://www.w3.org/ns/ldp#>
        PREFIX ns0: <https://carbonldp.com/ns/v1/platform#> 
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
        PREFIX ns1: <https://schema.org/>

        SELECT ?id
        WHERE {{
            <https://territoire.emse.fr/ldp/spsk/> ldp:hasMemberRelation ldp:member ;
            ldp:member ?id.
            ?id ns1:organizer ?o.
            ?id ns1:startDate ?date.
            FILTER (?date > now()).
            FILTER( regex(?o, "EMSE", "i"))
            FILTER (!regex(?o, "CPS2", "i"))
        }}
        """
                    )
    try:
        qres = sparql.queryAndConvert()
        for r in qres["results"]["bindings"]:
            print(r)
    except Exception as e:
        print(e)
    return qres

#R5 - AddAnAttendee
@app.route('/add_attendee', methods=['POST'])
def add_attendee():
        print("Adding Attendee")
        global rdf
        global rdfs
        global SCHEMA
        global ldp
        # form data has a dictionary structure
        #eventId = request.form.get("eventid")
        # attendeeName = request.form.get("attendeeName")
        # attendeeComment = request.form.get("attendeeComment")
        # loop through the dictionary and create a Blank node for the event and upload it to the ldp
        g = Graph()
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("schema", SCHEMA)
        g.bind("ldp", ldp)

        eventId = "https://territoire.emse.fr/ldp/spsk/ade60323032322d3230323353542d455449454e4e452d32313931332d302d31/"
        attendeeName = "soumya kumbar"
        attendeeComment = "I am attending"
        sparql.setQuery(f"""
            PREFIX ldp: <http://www.w3.org/ns/ldp#>
            PREFIX ns0: <https://carbonldp.com/ns/v1/platform#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX ns1: <https://schema.org/>
    
            SELECT *
            WHERE {{
                "{eventId}" a <https://schema.org/Event> ;
                <https://schema.org/location> ?location;
                <https://schema.org/startDate> ?startDate;
                <https://schema.org/startTime> ?startTime;
                <https://schema.org/endDate>   ?endDate;
                <https://schema.org/endTime>   ?endTime;
                <https://schema.org/organizer> ?organizer;
                <https://schema.org/name>      ?name;
                <https://schema.org/uid>        ?uid;
            }}
            """
                        )
        try:
            qres = sparql.queryAndConvert()
            print(qres)
            for r in qres["results"]["bindings"]:
                uid = r['uid']['value']
                startDate = r['startDate']['value']
                startTime = r['startTime']['value']
                endDate = r['endDate']['value']
                endTime = r['endTime']['value']
                location = r['location']['value']
                organizer = r['organizer']['value']
                name = r['name']['value']

            container = 'https://territoire.emse.fr/ldp/spsk/'
            username = "ldpuser"
            password = "LinkedDataIsGreat"

            rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
            rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
            SCHEMA = Namespace("https://schema.org/")
            SCHEMAComments = Namespace("https://schema.org/UserComments")
            SCHEMAPerson = Namespace("https://schema.org/Person")

            graph = Graph()

            graph.bind("rdf", rdf)
            graph.bind("rdfs", rdfs)
            graph.bind("schema", SCHEMA)

            schedule = URIRef(eventId)
            person = "ss"
            comment = "I am attending"

            person_graph = Graph()

            graph.add((schedule, rdf.type, SCHEMA.Event))
            graph.add((schedule, SCHEMA.startDate, Literal(startDate, datatype=XSD.date)))
            graph.add((schedule, SCHEMA.startTime, Literal(startTime, datatype=XSD.time)))
            graph.add((schedule, SCHEMA.endDate, Literal(endDate, datatype=XSD.date)))
            graph.add((schedule, SCHEMA.endTime, Literal(endTime, datatype=XSD.time)))
            graph.add((schedule, SCHEMA.location, Literal(location)))
            graph.add((schedule, SCHEMA.organizer, Literal(organizer, datatype=XSD.string)))
            graph.add((schedule, SCHEMA.name, Literal(name, datatype=XSD.string)))
            graph.add((schedule, SCHEMA.attendee, person_graph))
            graph.add((person_graph, SCHEMAPerson.givenName, Literal(person, datatype=XSD.string)))
            graph.add((person_graph, SCHEMAComments.commentText, Literal(comment, datatype=XSD.string)))
            headers = {
                'Content-type': 'text/turtle'
            }

            event = graph.serialize()
            response = requests.delete(eventId, headers=headers, auth=(username, password))
            response = requests.post(container, headers=headers, auth=(username, password), data=event)
        except Exception as e:
            print(e)
        return eventId

@app.route('/validateEvent', methods=['POST'])
def validateEvent():
    shape_graph = "EVENT_F.ttl"
    data_graph = "rdf_calender.ttl"
    r = validate(data_graph,
                 shacl_graph=shape_graph,
                 inference='rdfs',
                 data_graph_format="ttl",
                 shape_graph_format="ttl",
                 debug=False,
                 report_graph="ttl"
                 )
    conforms, report_graph, results_text = r

    print("Conforms: ", conforms)
    print("Report Graph: ", report_graph)
    print("Results text: ", results_text)
    return str(conforms)

if __name__ == "__main__":
    app.run(debug=True)

