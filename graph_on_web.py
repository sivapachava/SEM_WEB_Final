#To run our graph on the Web

from icalendar import Calendar
from rdflib import Graph, URIRef, Namespace, Literal, BNode
from flask import Flask

app = Flask(__name__)
@app.route('/caldata', methods = ['GET'])

def convertto_RDF():
        
        rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
        SCHEMA = Namespace("https://schema.org/")
        ldp = Namespace("http://www.w3.org/ns/ldp#")
        
        g = Graph()
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("schema", SCHEMA)
        g.bind("ldp", ldp)

        container = URIRef("https://territoire.emse.fr/ldp/spsk/")

        g.add((container, rdf.type, SCHEMA.Thing))
        g.add((container, rdf.type, SCHEMA.schedule))
        g.add((container, SCHEMA.description, Literal("The graph contains the representation of our university Calender events", lang = ("en"))))
        
        with open('ADECal.ics', 'r') as f:
            ecal = Calendar.from_ical(f.read())
            for component in ecal.walk():
             #event = BNode()
             if component.name == "VEVENT":
                
                description = component.decoded("DESCRIPTION").decode("utf-8").split()
                description = description[:-3]
                wdescription = ' '.join(description)
                uid = component.get("uid")
                url = "/{}".format(uid)
                schedule = URIRef( url )
                
                dtstart = str(component.decoded("dtstart")).split()
                dtstartdate = dtstart[0]
                #print(dtstartdate)
                dtstarttime = dtstart[1]
                #print(dtstarttime)
                
                dtend = str(component.decoded("dtend")).split()
                dtenddate = dtend[0]
                #print(dtenddate)
                dtendtime = dtend[1]
                #print(dtendtime)
                
                g.add((container, ldp.containes, schedule))
                g.add((schedule, rdf.type, SCHEMA.Event))
                g.add((schedule, SCHEMA.name, Literal(component.get("summary"))))
                g.add((schedule, SCHEMA.location, Literal(component.get("location"))))
                #g.add((schedule, SCHEMA.startDate, Literal(component.decoded("dtstart"))))
                #g.add((schedule, SCHEMA.endDate, Literal(component.decoded("dtend"))))
                g.add((schedule, SCHEMA.startDate, Literal(dtstartdate)))
                g.add((schedule, SCHEMA.startTime, Literal(dtstarttime)))
                g.add((schedule, SCHEMA.endDate, Literal(dtenddate)))
                g.add((schedule, SCHEMA.endTime, Literal(dtendtime)))
                g.add((schedule, SCHEMA.organizer, Literal(wdescription)))
                g.add((schedule, SCHEMA.uid, Literal(component.get("uid"))))
                #g.add((event, SCHEMA.duration, Literal("03:30")))
                #g.add((event, SCHEMA.Attendee, Literal("23")))

            f.close()
            return(g.serialize(format="ttl"))

convertto_RDF()

if __name__ == "__main__":
    app.run(debug=True)