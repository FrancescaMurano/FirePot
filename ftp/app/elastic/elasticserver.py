from elasticsearch import Elasticsearch
import os
# from elasticsearch_dsl import Q,Search
# IP = "34.17.54.125"
IP = os.getenv("IP_ELASTIC_KIBANA","localhost")

class ElasticServer:
    _instance = None

    def __new__(cls) -> None:
        if not  cls._instance:
            cls._instance = super(ElasticServer,cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self,'initialized'):
            self.initialized = True

            username = "elastic"
            password = "+RIk0Zh-KI=oJL*bkopF"

            self.es = Elasticsearch(f"http://{IP}:9200",
                    # ca_certs="config/certs/http_ca.crt",
                    basic_auth=(username,password))

    def insert_data(self,json_data):
        try:
            self.es.index(
                index='ftp_data',
                document=json_data
            )
        except Exception as e:
            print(str(e))
    
    def insert_info_ip(self, json_ip_data):
        try:
            self.es.index(
                index='info_ip_ftp',
                document=json_ip_data
            )
        except Exception as e:
            print(str(e))


