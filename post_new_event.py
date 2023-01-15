#To post new event to the https://territoire.emse.fr/ldp/spsk/ container.
#For every new event it will generate a new uid.
import requests
from  rdflib import Graph,Namespace, Literal, URIRef, XSD
import uuid

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

startDate = "2023-01-19"
startTime = "08:15:00+00:00"
endDate = "2023-01-19"
endTime = "10:15:00+00:00"
location = "EMSE S129,EMSE Espace Fauriel S1.32"
organizer = "M2 CPS2 NARDIN GUSTAVO"
name = "CM/TD Cloud and Edge Infrastructures"
uid = uuid.uuid4()
uid = "ade" + str(uid)
print(uid)
#schedule = URIRef("https://territoire.emse.fr/ldp/spsk/sample")
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
        'Content-type': 'text/turtle',
    }
    
event  = graph.serialize()

response = requests.post(container, headers=headers,  auth=(username, password), data=event)