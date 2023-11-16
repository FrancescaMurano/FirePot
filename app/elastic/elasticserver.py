from elasticsearch import Elasticsearch
import datetime

class ElasticServer:

    _instance = None

    def __new__(cls) -> None:
        if not  cls._instance:
            cls._instance = super(ElasticServer,cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self,'initialized'):
            self.initialized = True

            username = ""
            password = ""

            self.es = Elasticsearch("https://34.17.58.83:9200",
                    ca_certs="config/certs/http_ca.crt",
                    basic_auth=(username,password))


    def insert_ip_data(self,json_ip_data):
        self.es.index(
            index='ip_info',
            document=json_ip_data
    )
    def insert_ip_request(self,json_ip_requests):
        # add time
        json_ip_requests["time"] = datetime.datetime.now().time().replace(microsecond=0).isoformat()
        # add date 
        json_ip_requests["date"] =  datetime.datetime.now().date().isoformat()
        self.es.index(
            index='commands',
            document=json_ip_requests
    )


