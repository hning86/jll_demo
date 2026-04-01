# Multi-Cloud Property Agent Demo

This repository demonstrates a multi-cloud architecture showcasing a real estate property agent built using the **Google ADK (Agent Development Kit)**. The agent orchestrates tools across both Google Cloud Platform (GCP) and Microsoft Azure to answer user queries and manage property data.

## 📂 Repository Structure

The workspace consists of three primary services:

-   **[`property_agent/`](./property_agent)**: The central Python-based AI agent using Google ADK. It acts as the coordinator between the user and the multi-cloud data sources.
-   **[`gcp_mcp/`](./gcp_mcp)**: A Python-based Model Context Protocol (MCP) server exposing commercial real estate listings data hosted in Google Cloud.
-   **[`azure_mcp/`](./azure_mcp)**: An Azure Functions-based Model Context Protocol (MCP) server providing personalized user-facing features (such as saving, retrieving and removing favorite listings).

---

## 🗺️ Architecture Diagram

```mermaid
graph TD
    User(["User 🗣️"]) --> GE["Gemini Enterprise 🚀"]
    
    subgraph VAAE ["Vertex AI Agent Engine ⚙️"]
        PA["Property Agent 🤖 <br/> (Google ADK)"]
    end

    GE -- "Registered Agent" --> PA
    PA -->|Retrieve listings| GCP["GCP MCP ☁️ <br/> (GCP Clound Run)"]
    PA -->|Manage favorites| AZ["Azure MCP ☁️ <br/> (Azure Functions)"]
```

---

## 🏗 High-Level Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant GE as Gemini Enterprise
    participant VAAE as Vertex AI Agent Engine<br/>(Property Agent)
    participant GCP as GCP MCP Server<br/>(Listings)
    participant AZ as Azure MCP Server<br/>(Favorites)

    User->>GE: Asks a real estate query
    GE->>VAAE: Routes request to the registered Agent
    VAAE->>AZ: Retrieves favorite property IDs
    AZ-->>VAAE: Returns saved favorite IDs
    VAAE->>GCP: Fetches detailed listing data for IDs
    GCP-->>VAAE: Returns commercial listings data
    VAAE->>AZ: Persists new favorites (if requested)
    AZ-->>VAAE: Confirms state updated
    VAAE-->>GE: Synthesizes the multi-cloud data
    GE-->>User: Delivers the final formulated response
```

1. **Query**: The user submits a natural language request through **Gemini Enterprise**.
2. **Routing**: Gemini Enterprise routes the prompt to the registered **Property Agent** hosted on **Vertex AI Agent Engine**.
3. **Retrieve**: The agent dynamically calls the **GCP MCP** to find specific property details (address, price, type).
4. **Persist/View State**: The agent uses the **Azure MCP** to query or store personalized data like user favorites.
5. **Response**: The agent synthesizes the retrieved multi-cloud data and returns the final formulated answer to the user via Gemini Enterprise.

---

## ❓ Example Questions

Here are some sample interactive queries the agent is designed to handle across the multi-cloud setup:

-   🗣️ **General Exploration**: *"What are the commercial properties available under management?"*
-   🔍 **Detailed Inquiry**: *"Tell me more about property ID CRE1007."*
-   💾 **Personalization**: *"Save CRE1007 as one of my favorite properties."*
-   📋 **Retrieval**: *"Show me a list of my favorite properties."*

---

## 🚦 Getting Started

Each system is self-contained with its own set of dependencies and environment variables. To run the full demo session, refer to the deep-dive guides inside each folder:

-   👉 [Property Agent README](./property_agent/README.md)
-   👉 [GCP MCP README](./gcp_mcp/README.md)
-   👉 [Azure MCP README](./azure_mcp/README.md)
