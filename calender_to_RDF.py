from icalendar import Calendar
from rdflib import Graph, URIRef, Namespace, Literal, XSD

def convertto_RDF(fileName):
        file = "static\\uploads\\" + fileName
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
        
        with open(file, 'r') as f:
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
                g.add((schedule, SCHEMA.startDate, Literal(dtstartdate, datatype = XSD.date)))
                g.add((schedule, SCHEMA.startTime, Literal(dtstarttime, datatype = XSD.time)))
                g.add((schedule, SCHEMA.endDate, Literal(dtenddate, datatype = XSD.date)))
                g.add((schedule, SCHEMA.endTime, Literal(dtendtime, datatype = XSD.time)))
                g.add((schedule, SCHEMA.organizer, Literal(wdescription)))
                g.add((schedule, SCHEMA.uid, Literal(component.get("uid"))))
                #g.add((event, SCHEMA.duration, Literal("03:30")))
                #g.add((event, SCHEMA.Attendee, Literal("23")))

            f.close()
        print(g.serialize(r"rdf_cal_F.ttl", format="ttl"))
        


        



