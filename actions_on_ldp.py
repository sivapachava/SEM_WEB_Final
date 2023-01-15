
import requests
from rdflib import Graph, Namespace, URIRef, BNode, Literal, XSD

URL = "https://territoire.emse.fr/ldp/sivasoumya/"
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = Namespace("https://schema.org/")
schedule = URIRef("https://territoire.emse.fr/ldp/sivasoumya/")

def create_container(slug):
    #api endpoint
    headers = {'Content-Type': 'text/turtle', 'Slug': slug}
    xml_body = """<> a <http://example.org>."""
    r = requests.post(url=URL, headers=headers, auth=('ldpuser','LinkedDataIsGreat'), data=xml_body)
    pass

def uploadfile_to_ldp():
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
        endDate = g.value(event,SCHEMA.endDate)
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
        graph.add((schedule, SCHEMA.startDate, Literal(startDate)))  
        graph.add((schedule, SCHEMA.endDate, Literal(endDate)))
        graph.add((schedule, SCHEMA.location, Literal(location)))   
        graph.add((schedule, SCHEMA.organizer, Literal(director, datatype = XSD.string)))    
        graph.add((schedule, SCHEMA.name, Literal(name)))    
        
        headers = {
            'Content-type': 'text/turtle',
        }
        
        event  = graph.serialize()

        params = {'graph': graph_name}
        response = requests.post(container, headers=headers,  auth=(username, password), params=params, data=event)


    URL = "https://territoire.emse.fr/ldp/sivasoumya/"
    headers = {'Content-Type': 'text/turtle'}
    xml_body = """<> a <http://example.org>."""
    r = requests.post(url=URL, headers=headers, auth=('ldpuser', 'LinkedDataIsGreat'), data=xml_body)
    def add_event_to_ldp():
        # Create a BNode of these events
        g = Graph()
        g. bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("schema", SCHEMA)


        g.add((schedule, rdf.type, SCHEMA.Thing))
        g.add((schedule, rdf.type, SCHEMA.schedule))

        event = BNode()
        #associate Literals coming from Frontend to Literals here
        g.add((schedule, SCHEMA.subjectOf, event))
        g.add((event, rdf.type, SCHEMA.Event))
        g.add((event, SCHEMA.description, Literal("first class of semantic web coures")))
        g.add((event, SCHEMA.name, Literal("summary")))
        g.add((event, SCHEMA.location, Literal("location")))
        g.add((event, SCHEMA.startDate, Literal("dtstart")))
        g.add((event, SCHEMA.endDate, Literal("dtend")))
        g.add((event, SCHEMA.director, Literal("DESCRIPTION")))

        URL = "https://territoire.emse.fr/ldp/sivasoumya/"
        headers = {'Content-Type': 'text/turtle'}
        xml_body = """<> a <http://example.org>."""
        r = requests.post(url=URL, headers=headers, auth=('ldpuser', 'LinkedDataIsGreat'), data=xml_body)

def list_upcoming_events_ldp():
# SPARQLWrapper query to the ldp
    pass

def list_other_events_ldp():
# SPARQLWrapper query to the ldp
    pass

def add_attendee_to_ldp():
    # create an Attendee Node.
    # Associate information provided in the frontend to the Literals in this node
    URL = "https://territoire.emse.fr/ldp/sivasoumya/"
    headers = {'Content-Type': 'text/turtle'}
    xml_body = """<> a <http://example.org>."""
    r = requests.post(url=URL, headers=headers, auth=('ldpuser', 'LinkedDataIsGreat'), data=xml_body)

# POST attendee in the event
    pass









