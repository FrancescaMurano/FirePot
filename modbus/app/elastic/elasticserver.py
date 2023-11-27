from elasticsearch import Elasticsearch

IP = "34.17.54.125"
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

        
    def insert_modbus_connection_request(self,json):
        self.es.index(
            index='modbus_connection',
            document=json
    )

    def insert_modbus_log_request(self,json):
        self.es.index(
            index='modbus_log',
            document=json
    )    
        
