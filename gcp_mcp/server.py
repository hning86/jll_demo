import asyncio
import logging
import os
import json
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Commercial Properties MCP Server")

# load JSON from listings.json file
properties = json.load(open("listings.json"))

@mcp.tool()
def search_properties_by_type(property_type: str) -> List[Dict[str, Any]]:
    """
    Searches for commercial properties by property type.

    Args:
        property_type: The type of property (e.g., 'Office Building', 'Retail Space').

    Returns:
        A list of dictionaries, where each dictionary represents a property matching the criteria.
    """
    logger.info(
        f">>> 🛠️ Tool: 'search_properties_by_type' called with property_type='{property_type}'"
    )
    results = [
        p for p in properties if p["property_type"].lower() == property_type.lower()
    ]
    return results

@mcp.tool()
def get_property_types() -> List[str]:
    """
    Returns a list of unique property types available.

    Returns:
        A sorted list of strings, where each string is a unique property type.
    """
    logger.info(">>> 🛠️ Tool: 'get_property_types' called")
    property_types = set(p["property_type"] for p in properties)
    return sorted(list(property_types))


@mcp.tool()
def get_property_details(listing_id: str) -> Dict[str, Any]:
    """
    Retrieves the details of a specific property by its listing ID.

    Args:
        listing_id: The ID of the listing (e.g., 'CRE1001').

    Returns:
        A dictionary with the property's details or an empty dictionary if not found.
    """
    logger.info(f">>> 🛠️ Tool: 'get_property_details' called for '{listing_id}'")
    for prop in properties:
        if prop["listing_id"].lower() == listing_id.lower():
            return prop
    return {}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"🚀 MCP server started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )