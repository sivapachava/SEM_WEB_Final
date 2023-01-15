from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper('https://territoire.emse.fr/ldp/')
sparql.setReturnFormat(JSON)
sparql.setCredentials("ldpuser", "LinkedDataIsGreat")

#To get all events related to https://territoire.emse.fr/ldp/spsk/ on LDP container.
sparql.setQuery("""
    PREFIX ldp: <http://www.w3.org/ns/ldp#>
    PREFIX ns0: <https://carbonldp.com/ns/v1/platform#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX schema: <https://schema.org/#>
    
    SELECT *
    WHERE {
        ?s a <https://schema.org/Event> ;
        <https://schema.org/location> ?location;
        <https://schema.org/startDate> ?startDate;
        <https://schema.org/startTime> ?startTime;
        <https://schema.org/endDate>   ?endDate;
        <https://schema.org/endTime>   ?endTime;
        <https://schema.org/organizer> ?organizer;
        <https://schema.org/name>      ?name;
        <https://schema.org/uid>        ?uid.

        }
        LIMIT 10
     """
)
try:
    qres = sparql.queryAndConvert()
    
    for r in qres["results"]["bindings"]:
        print(r)
except Exception as e :
    print(e)