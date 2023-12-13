set VALORE1=2222

docker-compose -f docker-compose_ssh.yml build && docker-compose -f docker-compose_ssh.yml -f docker-compose_elastic_kibana.yml up -d
