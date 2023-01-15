from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper('https://territoire.emse.fr/ldp/')
sparql.setReturnFormat(JSON)
sparql.setCredentials("ldpuser", "LinkedDataIsGreat")

#To get all upcoming events
sparql.setQuery("""
    PREFIX ldp: <http://www.w3.org/ns/ldp#>
    PREFIX ns0: <https://carbonldp.com/ns/v1/platform#> 
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    PREFIX ns1: <https://schema.org/>
        
    SELECT *
    WHERE {
        <https://territoire.emse.fr/ldp/spsk/> ldp:hasMemberRelation ldp:member ;
        ldp:member ?id .
        ?id ns1:organizer ?organizer;
            ns1:name      ?name;
            ns1:location  ?location;
            ns1:startDate ?startDate.
            
        FILTER(?startDate > NOW())    
    }
    LIMIT 10
    """ 
)

#For get events on particular date in the container
#FILTER(?startDate = "2022-12-09"^^xsd:date )

try:
    qres = sparql.queryAndConvert()
        
    for r in qres["results"]["bindings"]:
        print(r)
except Exception as e :
    print(e)
    

