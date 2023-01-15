#To post all our events in graph to LDP container
import requests
from  rdflib import Graph,Namespace, Literal, URIRef, XSD

container = 'https://territoire.emse.fr/ldp/spsk/'
graph_name = 'rdf_cal_F.ttl'
username = "ldpuser"
password = "LinkedDataIsGreat"

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = Namespace("https://schema.org/")
ldp = Namespace("http://www.w3.org/ns/ldp#")



g = Graph().parse("C:\\Users\\Siva Ratnam Pachava\\OneDrive\Desktop\\SemW P\\SemWeb\\rdf_cal_F.ttl")
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)
g.bind("schema", SCHEMA)
g.bind("ldp", ldp)


for event in g.subjects(rdf.type,SCHEMA.Event):
    print(event)


    startDate  = g.value(event,SCHEMA.startDate)
    startTime = g.value(event,SCHEMA.startTime)
    endDate = g.value(event,SCHEMA.endDate)
    endTime = g.value(event,SCHEMA.endTime)
    location = g.value(event,SCHEMA.location)
    director  = g.value(event,SCHEMA.organizer)
    #print(director)
    uid = g.value(event,SCHEMA.uid)
    #print(uid)
    name  = g.value(event,SCHEMA.name)
    
    schedule_url = "/{}".format(uid)
    schedule = URIRef( schedule_url )
    
    graph = Graph()
    #graph.add((schedule, ldp.containes, event))
    graph.add((schedule, rdf.type, SCHEMA.Event))
    graph.add((schedule, SCHEMA.uid, Literal(uid)))
    graph.add((schedule, SCHEMA.startDate, Literal(startDate, datatype = XSD.date)))
    graph.add((schedule, SCHEMA.startTime, Literal(startTime, datatype = XSD.time)))
    graph.add((schedule, SCHEMA.endDate, Literal(endDate, datatype = XSD.date)))
    graph.add((schedule, SCHEMA.endTime, Literal(endTime, datatype = XSD.time)))
    graph.add((schedule, SCHEMA.location, Literal(location)))   
    graph.add((schedule, SCHEMA.organizer, Literal(director, datatype = XSD.string)))    
    graph.add((schedule, SCHEMA.name, Literal(name)))    
    
    headers = {
        'Content-type': 'text/turtle',
    }
    
    event  = graph.serialize()

    params = {'graph': graph_name}
    response = requests.post(container, headers=headers,  auth=(username, password), params=params, data=event)