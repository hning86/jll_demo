# cd ~/mcp-example/mcp-on-cloudrun
gcloud run deploy properties-mcp-server \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=.