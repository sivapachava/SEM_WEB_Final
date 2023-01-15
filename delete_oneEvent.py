#To delete one particular event in the https://territoire.emse.fr/ldp/spsk/ container
import requests
from  rdflib import Graph,Namespace, Literal, URIRef, XSD
import uuid

container = 'https://territoire.emse.fr/ldp/spsk/'
username = "ldpuser"
password = "LinkedDataIsGreat"
schedule_url = "https://territoire.emse.fr/ldp/spsk/ade60323032322d3230323353542d455449454e4e452d32323533302d302d3131/"


headers = {
        'Content-type': 'text/turtle',
    }
    

response = requests.delete(schedule_url, headers=headers,  auth=(username, password))

