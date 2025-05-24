import datetime
import json
import os
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.generativeai import GenerativeModel
from google.genai import types
import vertexai
from vertexai.preview import reasoning_engines

# Constants for Kenya's coastal mangrove species
KENYA_MANGROVE_SPECIES = {
    "rhizophora mucronata": {
        "swahili_name": "Mkoko",
        "characteristics": "Distinctive prop roots, elongated propagules",
        "uses": "Timber, firewood, boat building",
        "conservation_status": "Vulnerable in many areas"
    },
    "avicennia marina": {
        "swahili_name": "Mchu",
        "characteristics": "Grey-green leaves, pencil-like pneumatophores",
        "uses": "Medicinal purposes, honey production",
        "conservation_status": "Relatively stable"
    },
    "sonneratia alba": {
        "swahili_name": "Mlilana",
        "characteristics": "White flowers, round fruits, conical pneumatophores",
        "uses": "Fruits are edible, wood for construction",
        "conservation_status": "Declining in some areas"
    },
    "ceriops tagal": {
        "swahili_name": "Mkandaa",
        "characteristics": "Small tree, club-shaped propagules with ridges",
        "uses": "Dye production, poles for construction",
        "conservation_status": "Threatened by harvesting"
    },
    "bruguiera gymnorrhiza": {
        "swahili_name": "Muia",
        "characteristics": "Knee-like roots, red flowers, long propagules",
        "uses": "Construction, charcoal production",
        "conservation_status": "Vulnerable"
    }
}

# Coastal regions in Kenya with significant mangrove forests
KENYA_COASTAL_REGIONS = {
    "mida creek": {
        "county": "Kilifi",
        "mangrove_area_hectares": 1600,
        "dominant_species": ["rhizophora mucronata", "avicennia marina"],
        "threats": ["Tourism development", "Wood harvesting", "Climate change"]
    },
    "gazi bay": {
        "county": "Kwale",
        "mangrove_area_hectares": 615,
        "dominant_species": ["rhizophora mucronata", "sonneratia alba", "ceriops tagal"],
        "threats": ["Overharvesting", "Sedimentation", "Coastal erosion"]
    },
    "lamu archipelago": {
        "county": "Lamu",
        "mangrove_area_hectares": 34000,
        "dominant_species": ["rhizophora mucronata", "avicennia marina", "bruguiera gymnorrhiza"],
        "threats": ["Port development", "Oil exploration", "Deforestation"]
    },
    "vanga": {
        "county": "Kwale",
        "mangrove_area_hectares": 4000,
        "dominant_species": ["rhizophora mucronata", "avicennia marina"],
        "threats": ["Border disputes", "Illegal cutting", "Pollution"]
    },
    "mombasa": {
        "county": "Mombasa",
        "mangrove_area_hectares": 1900,
        "dominant_species": ["avicennia marina", "sonneratia alba"],
        "threats": ["Urban expansion", "Pollution", "Port activities"]
    }
}
# Core Agent Functions

def identify_mangrove_species(species_name: str) -> dict:
    """
    Identifies a mangrove species and provides information about it.
    
    Args:
        species_name (str): Common or scientific name of the mangrove species.
        
    Returns:
        dict: Information about the species or error message.
    """
    species_name_lower = species_name.lower()
    
    # Check direct matches
    if species_name_lower in KENYA_MANGROVE_SPECIES:
        info = KENYA_MANGROVE_SPECIES[species_name_lower]
        return {
            "status": "success",
            "report": {
                "species": species_name.title(),
                "swahili_name": info["swahili_name"],
                "characteristics": info["characteristics"],
                "uses": info["uses"],
                "conservation_status": info["conservation_status"]
            }
        }
    
    # Check partial matches
    for name, info in KENYA_MANGROVE_SPECIES.items():
        if species_name_lower in name or name in species_name_lower:
            return {
                "status": "success",
                "report": {
                    "species": name.title(),
                    "swahili_name": info["swahili_name"],
                    "characteristics": info["characteristics"],
                    "uses": info["uses"],
                    "conservation_status": info["conservation_status"]
                }
            }
        if info["swahili_name"].lower() == species_name_lower:
            return {
                "status": "success",
                "report": {
                    "species": name.title(),
                    "swahili_name": info["swahili_name"],
                    "characteristics": info["characteristics"],
                    "uses": info["uses"],
                    "conservation_status": info["conservation_status"]
                }
            }
    
    return {
        "status": "error",
        "error_message": f"Could not identify mangrove species '{species_name}'. Please try using scientific name or Swahili name."
    }

def get_site_information(location: str) -> dict:
    """
    Provides information about mangrove forests in a specific coastal location.
    
    Args:
        location (str): Name of the coastal area in Kenya.
        
    Returns:
        dict: Information about the mangrove site or error message.
    """
    location_lower = location.lower()
    
    # Check direct matches
    if location_lower in KENYA_COASTAL_REGIONS:
        info = KENYA_COASTAL_REGIONS[location_lower]
        
        # Get dominant species information
        species_info = []
        for species in info["dominant_species"]:
            if species in KENYA_MANGROVE_SPECIES:
                species_info.append({
                    "name": species.title(),
                    "swahili_name": KENYA_MANGROVE_SPECIES[species]["swahili_name"]
                })
        
        return {
            "status": "success",
            "report": {
                "location": location.title(),
                "county": info["county"],
                "mangrove_area_hectares": info["mangrove_area_hectares"],
                "dominant_species": species_info,
                "threats": info["threats"]
            }
        }
    
    # Check partial matches
    for name, info in KENYA_COASTAL_REGIONS.items():
        if location_lower in name or name in location_lower or info["county"].lower() == location_lower:
            species_info = []
            for species in info["dominant_species"]:
                if species in KENYA_MANGROVE_SPECIES:
                    species_info.append({
                        "name": species.title(),
                        "swahili_name": KENYA_MANGROVE_SPECIES[species]["swahili_name"]
                    })
            
            return {
                "status": "success",
                "report": {
                    "location": name.title(),
                    "county": info["county"],
                    "mangrove_area_hectares": info["mangrove_area_hectares"],
                    "dominant_species": species_info,
                    "threats": info["threats"]
                }
            }
    
    return {
        "status": "error",
        "error_message": f"Information about mangroves in '{location}' is not available in our database."
    }

# Carborn Storage Calculator 

def calculate_carbon_storage(area: float, forest_age: str = "mature") -> dict:
    """
    Estimates carbon storage potential of a mangrove forest area.
    
    Args:
        area (float): Area of mangrove forest in hectares.
        forest_age (str): Age classification of the forest (young, middle-aged, mature).
        
    Returns:
        dict: Carbon storage estimates or error message.
    """
    # Basic validation
    if not isinstance(area, (int, float)) or area <= 0:
        return {
            "status": "error",
            "error_message": "Please provide a valid positive number for area in hectares."
        }
    
    # Carbon storage rates per hectare based on research in Kenya
    # These are simplified estimates for educational purposes
    carbon_rates = {
        "young": 143,       # Tons of carbon per hectare
        "middle-aged": 297, # Tons of carbon per hectare
        "mature": 392       # Tons of carbon per hectare
    }
    
    forest_age = forest_age.lower()
    if forest_age not in carbon_rates:
        forest_age = "mature"  # Default to mature if age is not recognized
    
    carbon_per_hectare = carbon_rates[forest_age]
    total_carbon = area * carbon_per_hectare
    co2_equivalent = total_carbon * 3.67  # Convert carbon to CO2 equivalent
    
    # Economic value (using simplified carbon credit value)
    carbon_credit_value_usd = co2_equivalent * 15  # Assuming $15 per ton of CO2
    
    return {
        "status": "success",
        "report": {
            "area_hectares": area,
            "forest_age": forest_age,
            "carbon_per_hectare_tons": carbon_per_hectare,
            "total_carbon_tons": total_carbon,
            "co2_equivalent_tons": co2_equivalent,
            "potential_carbon_credit_value_usd": carbon_credit_value_usd,
            "note": "These are estimates based on general studies of Kenyan mangroves. Actual values may vary based on species composition, health, and local conditions."
        }
    }

# Restoration Planning Function 

def plan_restoration(area_hectares: float, location: Optional[str] = None) -> dict:
    """
    Provides a restoration plan for a mangrove area.
    
    Args:
        area_hectares (float): Area to be restored in hectares.
        location (str, optional): Specific coastal location for customized recommendations.
        
    Returns:
        dict: Restoration plan or error message.
    """
    if not isinstance(area_hectares, (int, float)) or area_hectares <= 0:
        return {
            "status": "error",
            "error_message": "Please provide a valid positive number for area in hectares."
        }
    
    # Base cost estimates per hectare (in Kenyan Shillings)
    base_costs = {
        "site_preparation": 25000,
        "seedling_production": 40000,
        "planting": 35000,
        "monitoring_first_year": 20000,
        "community_engagement": 15000
    }
    
    # Calculate basic costs
    total_cost = sum(base_costs.values()) * area_hectares
    seedlings_needed = int(area_hectares * 2000)  # Assuming 2000 seedlings per hectare
    
    # Default species recommendations
    recommended_species = ["Rhizophora mucronata", "Avicennia marina", "Sonneratia alba"]
    timeline_months = 24
    special_considerations = []
    
    # Customize based on location if provided
    if location:
        location_lower = location.lower()
        if location_lower in KENYA_COASTAL_REGIONS:
            info = KENYA_COASTAL_REGIONS[location_lower]
            
            # Recommend local dominant species
            recommended_species = [s.title() for s in info["dominant_species"]]
            
            # Add location-specific considerations
            if "Urban expansion" in info["threats"] or "Pollution" in info["threats"]:
                special_considerations.append("Community waste management education essential")
                total_cost += 10000 * area_hectares  # Additional cost for pollution mitigation
            
            if "Tourism development" in info["threats"]:
                special_considerations.append("Ecotourism integration recommended")
                timeline_months = 30  # Longer timeline for tourism integration
            
            if "Sedimentation" in info["threats"]:
                special_considerations.append("Soil erosion control measures required upland")
                total_cost += 15000 * area_hectares  # Additional cost for erosion control
    
    # Convert to USD for international context (approximate exchange rate)
    cost_usd = total_cost / 130  # Approximate KES to USD conversion
    
    return {
        "status": "success",
        "report": {
            "area_hectares": area_hectares,
            "location": location.title() if location else "Generic plan",
            "recommended_species": recommended_species,
            "seedlings_needed": seedlings_needed,
            "estimated_timeline_months": timeline_months,
            "estimated_cost_kes": total_cost,
            "estimated_cost_usd": cost_usd,
            "special_considerations": special_considerations,
            "community_involvement": "Recommended to engage local community members in seedling production, planting, and monitoring to ensure long-term sustainability.",
            "next_steps": [
                "1. Conduct detailed site assessment",
                "2. Engage local community stakeholders",
                "3. Secure necessary permits from Kenya Forest Service",
                "4. Establish community nursery for seedling production",
                "5. Implement planting according to lunar calendar (best during spring tides)"
            ]
        }
    }

def answer_general_question(question: str) -> dict:
    """
    Answers general questions about mangroves, forests, and carbon credits using Gemini.
    
    Args:
        question (str): The question about mangroves, forests or carbon credits
        
    Returns:
        dict: Answer with information from the model
    """
    try:
        # Initialize the Gemini model
        model = GenerativeModel(model_name="gemini-2.0-flash")
        
        # Create a prompt that frames the context
        prompt = f"""
        As a mangrove conservation expert, please answer this question:
        {question}
        
        Focus on providing accurate, educational information about mangroves, their ecosystems, 
        conservation efforts, and carbon benefits. Include scientific facts where relevant.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        
        return {
            "status": "success",
            "report": {
                "question": question,
                "answer": response.text
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unable to answer general question: {str(e)}"
        }

# Create the Mangrove Protection System Agent
root_agent = Agent(
    name="mikoko_guardian",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent supporting mangrove conservation and restoration in coastal Kenya. "
        "Provides information on mangrove species, restoration planning, and carbon benefits."
        "Provides answers to general questions about mangroves, forests, and carbon credits."
        "Supports conservation efforts and community engagement and promotes sustainable practices to support the conversation of mangroove trees."
    ),
    instruction=""" You are Mikoko Guardian, an assistant for mangrove conservation in the coastal region of Kenya. 
        You can:
            1. Identify mangrove species, provide information about mangrove sites.
            2. Calculate carbon storage benefits, and help plan restoration projects. 
            3. Answer anything about Kenya's mangroves and general questions around magroove and carbon credit and enviromental conservation!
        Only answer questions related to mangroves, forests, carbon credits, carbon sinks and enviromental conversation efforts focused on the coastal region of Kenya.
        You can handle tasks sequentially if needed
    """,
    tools=[
        identify_mangrove_species, 
        get_site_information,
        calculate_carbon_storage,
        plan_restoration,
        answer_general_question
    ],
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2, # More deterministic output
        max_output_tokens=250
    )
)