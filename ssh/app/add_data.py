from elastic.elasticserver import ElasticServer
from utils.utils_ip_info import get_ip_info

e = ElasticServer()
data = e.insert_ip_data(get_ip_info("1.10.10.255"))
data = e.insert_ip_data(get_ip_info("1.10.11.255"))
data = e.insert_ip_data(get_ip_info("1.10.12.255"))
data = e.insert_ip_data(get_ip_info("1.10.13.255"))
data = e.insert_ip_data(get_ip_info("1.10.14.255"))
