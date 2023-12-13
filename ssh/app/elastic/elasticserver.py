from elasticsearch import Elasticsearch

IP = "localhost"
class ElasticServer:
    _instance = None

    def __new__(cls) -> None:
        if not  cls._instance:
            cls._instance = super(ElasticServer,cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self,'initialized'):
            self.initialized = True

            self.es = Elasticsearch(f"http://{IP}:9200",
                    # ca_certs="config/certs/http_ca.crt",
                    )

    def insert_ip_data(self,json_ip_data):
        try:
            self.es.index(
            index='info_ip_ssh',
            document=json_ip_data
        )
        except Exception as e:
            print(str(e))

    def insert_ip_request(self,json_ip_requests):
        try:
         self.es.index(
            index='commands_ssh',
            document=json_ip_requests)
        except Exception as e:
            print(str(e))
    

#     def erase(self):
#         query = Q('match',ipAddress='127.0.0.1')
#         s = Search(using=self.es).query(query)
#         responses = s.execute()
#         print(responses)
#         for hit in responses:
#             print(hit)
#             #self.es.delete(index="commands_ssh",id=hit.meta.id)


