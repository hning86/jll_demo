# update an existing instance
uv run adk deploy agent_engine \
--agent_engine_id 1547157995815698432 \
--display_name "Property Agent" \
--staging_bucket=gs://ninghai-temp-bucket property_agent

# deploy a new instance
#uv run adk deploy agent_engine \
#--display_name "Property Agent" \
#--staging_bucket=gs://ninghai-temp-bucket property_agent