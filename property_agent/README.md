# Property Agent

A commercial real estate property agent built using the Google ADK (Agent Development Kit). This agent acts as a helpful assistant that can retrieve property data from GCP and Azure MCP servers.

## Features

-   **GCP MCP Integration**: Retrieves specific property data such as address, property type, price, etc.
-   **Azure MCP Integration**: Greets users, saves favorite property IDs, and retrieves them later.
-   **Natural Language Interaction**: Answers questions about properties and adds colorful descriptions based on inferred data.

## Setup and Installation

The project uses `uv` for dependency management.

### Project Structure

```text
property_agent/
├── deploy.sh
├── main.py
├── pyproject.toml
└── property_agent/
    ├── .env
    ├── __init__.py
    └── agent.py
```

### Dependencies

Specified in `pyproject.toml`:
-   `google-adk>=1.20.0`

Additional libraries used:
-   `python-dotenv`
-   `google-cloud-logging`

### Environment Variables

The agent relies on a `.env` file in the `property_agent/property_agent` directory to configure its connections and model:

```bash
MODEL=... # The Gemini model to use (e.g., gemini-2.5-pro)
MCP_SERVER_URL=... # The URL of the GCP MCP server
AZURE_MCP_SERVER_URL=... # The URL of the Azure MCP server
AZURE_MCP_SERVER_KEY=... # The API key for the Azure MCP server
```

## Deployment

The agent can be deployed to Vertex AI Agent Engine using the provided `deploy.sh` script:

```bash
./deploy.sh
```

The script runs the `adk deploy agent_engine` command. Make sure to update the `--agent_engine_id` or other configuration flags as needed.
