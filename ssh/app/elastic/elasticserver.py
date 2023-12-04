from elasticsearch import AsyncElasticsearch
# from elasticsearch_dsl import Q,Search

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

            self.es = AsyncElasticsearch(f"http://{IP}:9200",
                    # ca_certs="config/certs/http_ca.crt",
                    basic_auth=(username,password))

    async def insert_ip_data(self,json_ip_data):
        await self.es.index(
            index='info_ip_ssh',
            document=json_ip_data
        )

    async def insert_ip_request(self,json_ip_requests):
        await self.es.index(
            index='commands_ssh',
            document=json_ip_requests
    )
    

#     def erase(self):
#         query = Q('match',ipAddress='127.0.0.1')
#         s = Search(using=self.es).query(query)
#         responses = s.execute()
#         print(responses)
#         for hit in responses:
#             print(hit)
#             #self.es.delete(index="commands_ssh",id=hit.meta.id)


# e = ElasticServer()
# e.erase()
