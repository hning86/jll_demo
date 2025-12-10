"""
Generates a list of dictionaries, each representing a commercial real estate property.
"""

import random
import json

def generate_cre_dataset(num_properties=40):
    """
    Generates a list of dictionaries, each representing a commercial real estate property.

    Args:
        num_properties: The number of properties to generate in the dataset.

    Returns:
        A list of dictionaries, where each dictionary is a property listing.
    """

    # Possible attributes for the properties
    districts = ["Financial District", "Tech Corridor", "Waterfront District", "Historic Quarter", "Industrial Park", "Downtown Core"]
    street_names = ["Main St", "Oak Ave", "Innovation Drive", "Market St", "River Rd", "Commerce Blvd"]
    status_options = ["For Sale", "For Lease"]

    property_type_map = {
        "Office Building": {
            "districts": ["Financial District", "Tech Corridor", "Downtown Core"],
            "size_range_sqft": (10000, 200000),
            "price_per_sqft_range": (400, 950) # Sale price
        },
        "Retail Space": {
            "districts": ["Waterfront District", "Historic Quarter", "Downtown Core"],
            "size_range_sqft": (1200, 15000),
            "price_per_sqft_range": (35, 110) # Annual lease rate
        },
        "Industrial Warehouse": {
            "districts": ["Industrial Park", "Tech Corridor"],
            "size_range_sqft": (50000, 500000),
            "price_per_sqft_range": (90, 250) # Sale price
        },
        "Mixed-Use Property": {
            "districts": ["Downtown Core", "Historic Quarter", "Financial District"],
            "size_range_sqft": (25000, 150000),
            "price_per_sqft_range": (300, 700) # Sale price
        },
    }

    list_of_property_types = list(property_type_map.keys())
    cre_properties = []

    for i in range(num_properties):
        # Choose a random property type
        prop_type = random.choice(list_of_property_types)
        prop_info = property_type_map[prop_type]

        # Generate realistic size and price
        size = random.randint(prop_info["size_range_sqft"][0] // 100, prop_info["size_range_sqft"][1] // 100) * 100
        price_per_sqft = random.randint(prop_info["price_per_sqft_range"][0], prop_info["price_per_sqft_range"][1])
        listing_price = size * price_per_sqft
        
        # Determine status (Retail is more likely to be for lease)
        status = "For Lease" if prop_type == "Retail Space" and random.random() < 0.7 else random.choice(status_options) # 70% chance for retail to be for lease

        # Create a new property dictionary
        property_listing = {
            "listing_id": f"CRE{1001 + i}",
            "property_type": prop_type,
            "address": f"{random.randint(10, 2000)} {random.choice(street_names)}",
            "district": random.choice(prop_info["districts"]),
            "size_sqft": size,
            "listing_price": listing_price,
            "status": status,
        }
        cre_properties.append(property_listing)

    return cre_properties

# --- Main Execution ---
CRE_PROPERTIES = generate_cre_dataset(40)

# Print the dataset in a readable JSON format
print(json.dumps(CRE_PROPERTIES, indent=4))
