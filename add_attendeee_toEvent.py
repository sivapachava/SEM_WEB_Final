#Add attendee information to the one particulat event. (To represent that the person attend the event.)
from SPARQLWrapper import SPARQLWrapper, JSON
from  rdflib import Graph,Namespace, Literal, URIRef, XSD
import requests

sparql = SPARQLWrapper('https://territoire.emse.fr/ldp/')
sparql.setReturnFormat(JSON)
sparql.setCredentials("ldpuser", "LinkedDataIsGreat")
eventId = "https://territoire.emse.fr/ldp/spsk/ade60323032322d3230323353542d455449454e4e452d32313931332d302d31/"

sparql.setQuery("""
    PREFIX ldp: <http://www.w3.org/ns/ldp#>
    PREFIX ns0: <https://carbonldp.com/ns/v1/platform#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    PREFIX ns1: <https://schema.org/>
    
    SELECT *
    WHERE {
        <https://territoire.emse.fr/ldp/spsk/ade60323032322d3230323353542d455449454e4e452d31303336372d302d30/> a <https://schema.org/Event> ;
        <https://schema.org/location> ?location;
        <https://schema.org/startDate> ?startDate;
        <https://schema.org/startTime> ?startTime;
        <https://schema.org/endDate>   ?endDate;
        <https://schema.org/endTime>   ?endTime;
        <https://schema.org/organizer> ?organizer;
        <https://schema.org/name>      ?name;
        <https://schema.org/uid>        ?uid;    
    }
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

    print(uid, startDate, startTime, endDate, endTime, location, organizer, name)
    
    container = 'https://territoire.emse.fr/ldp/spsk/'
    username = "ldpuser"
    password = "LinkedDataIsGreat"

    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    SCHEMA = Namespace("https://schema.org/")
    SCHEMAComments = Namespace("https://schema.org/UserComments")
    SCHEMAPerson = Namespace("https://schema.org/Person")

    graph= Graph()

    graph.bind("rdf", rdf)
    graph.bind("rdfs", rdfs)
    graph.bind("schema", SCHEMA)



    schedule = URIRef( eventId )
    person = "ss"
    comment = "I am attending"

    person_graph = Graph()


    graph.add((schedule, rdf.type, SCHEMA.Event))
    graph.add((schedule, SCHEMA.startDate, Literal(startDate, datatype = XSD.date)))
    graph.add((schedule, SCHEMA.startTime, Literal(startTime, datatype = XSD.time)))
    graph.add((schedule, SCHEMA.endDate, Literal(endDate, datatype = XSD.date)))
    graph.add((schedule, SCHEMA.endTime, Literal(endTime, datatype = XSD.time)))
    graph.add((schedule, SCHEMA.location, Literal(location)))   
    graph.add((schedule, SCHEMA.organizer, Literal(organizer, datatype = XSD.string)))    
    graph.add((schedule, SCHEMA.name, Literal(name, datatype = XSD.string)))    
    graph.add((schedule, SCHEMA.attendee, person_graph))  
    graph.add((person_graph, SCHEMAPerson.givenName, Literal(person, datatype = XSD.string)))  
    graph.add((person_graph, SCHEMAComments.commentText, Literal(comment, datatype = XSD.string)))

    print("Creating Graph to POST")
    headers = {
            'Content-type': 'text/turtle'
        }
        
    event  = graph.serialize()
    #print(event)
    response = requests.delete(eventId, headers=headers,  auth=(username, password))

    response = requests.post(container, headers=headers,  auth=(username, password), data=event)
    #print("POST request sent to the container ", response)
        
except Exception as e :
    print(e)
    

