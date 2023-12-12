#!/bin/bash

KIBANA_HOST="localhost"
KIBANA_PORT="5601"

# Indica il file JSON della dashboard
DASHBOARD_FILE="/dashboards/ftp_dashboard.ndjson"

# Componi l'URL per l'API di Kibana
# KIBANA_API_URL="http://${KIBANA_HOST}:${KIBANA_PORT}/api/saved_objects/_import"

# Invia la richiesta di importazione usando curl
# curl -X POST "${KIBANA_API_URL}" -H "kbn-xsrf: true" --form file=@${DASHBOARD_FILE}

cat "${DASHBOARD_FILE}"