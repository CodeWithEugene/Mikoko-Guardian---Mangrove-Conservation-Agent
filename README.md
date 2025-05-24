# Mikoko Guardian - Mangrove Conservation Agent

## Overview of the Agent

The Mikoko Guardian agent is a specialized AI assistant that supports mangrove conservation efforts in coastal Kenya. It provides educational information about mangrove species, coastal sites, carbon storage benefits, and restoration planning guidance. The agent helps conservationists, educators, researchers, and local communities access knowledge that promotes sustainable management of these critical coastal ecosystems.

## Agent Details

The mikoko_guardian agent has the following capabilities:

* **Mangrove Species Identification**: Identifies and provides detailed information about Kenya's coastal mangrove species including local Swahili names, characteristics, traditional uses, and conservation status.
* **Site Information**: Provides data on specific coastal regions in Kenya with significant mangrove forests, including area coverage, dominant species, and local threats.
* **Carbon Storage Calculation**: Estimates the carbon storage potential and equivalent carbon credit value of mangrove forests based on area and forest maturity.
* **Restoration Planning**: Generates customized restoration plans with species recommendations, resource requirements, timeline estimates, and cost projections.
* **General Knowledge Support**: Answers educational questions about mangroves, their ecosystems, and conservation practices using generative AI.

## Architecture

```
mikoko_guardian/
├── __init__.py
├── agent.py        # Core agent implementation with tools and data
└── .env
```

## Key Features

The key features of the mikoko_guardian agent include:

* **Environment**: 
  The agent operates with a focused dataset on Kenya's coastal mangrove ecosystems, including five major species and five significant coastal regions.

* **Memory**: 
  The agent maintains conversational context to provide coherent responses across multi-turn interactions.

* **Tools**:
  - `identify_mangrove_species`: Retrieves detailed information about mangrove species
  - `get_site_information`: Provides data on coastal regions with mangrove forests
  - `calculate_carbon_storage`: Estimates carbon storage and potential carbon credit value
  - `plan_restoration`: Generates customized restoration plans with resource estimates
  - `answer_general_question`: Handles educational questions about mangrove conservation

* **Complexity**: Easy

* **Agent Type**: Single Agent

* **Components**:
  - Species and site information database
  - Carbon calculation models
  - Restoration planning framework
  - Integration with Gemini 2.0 Flash for general knowledge

* **Vertical**: Environmental Conservation

## Example Interaction

```
User: "Hello! Can you tell me about mangrove species in Kenya?"

Agent: "I'd be happy to help with information about mangrove species in Kenya! The coastal region of Kenya has five main mangrove species:

1. Rhizophora mucronata (Mkoko) - Known for its distinctive prop roots and elongated propagules
2. Avicennia marina (Mchu) - Features grey-green leaves and pencil-like pneumatophores
3. Sonneratia alba (Mlilana) - Recognized by white flowers and round fruits
4. Ceriops tagal (Mkandaa) - A small tree with club-shaped propagules
5. Bruguiera gymnorrhiza (Muia) - Has knee-like roots and red flowers

Would you like more specific information about any of these species, or details about where they grow along Kenya's coast?"

User: "Tell me more about Mkoko species."

Agent: "Here's information about the Mkoko species:

Scientific Name: Rhizophora mucronata
Swahili Name: Mkoko
Characteristics: Distinctive prop roots, elongated propagules
Uses: Timber, firewood, boat building
Conservation Status: Vulnerable in many areas

Rhizophora mucronata is one of the most important mangrove species in Kenya's coastal ecosystems. Its complex prop root system provides critical habitat for marine life and helps prevent coastal erosion. The species is threatened in some areas due to over-harvesting and coastal development. Would you like to know about specific conservation efforts for this species or where it's commonly found along the Kenyan coast?"
```

### Getting the Code 📥

Now, let's obtain the bytewise code from GitHub:

Open your terminal or command prompt and navigate to the directory where you want to store the project. Then, use the following command to clone the repository:

```bash
# Clone using HTTPS
git clone https://github.com/mwanyumba7/mikoko-guardian
```

Alternatively, if you have configured SSH keys for GitHub, you can use:

```bash
# Clone using SSH
git clone git@github.com:mwanyumba7/mikoko-guardian
```

## Setup and Installation

1. **Prerequisites**:
   * Python 3.10 or newer
   * Google Cloud account for deployment (optional)

2. **Environment Setup**:
   ```bash
   # Create and activate virtual environment
   python -m venv agent-venv
   
   # For Windows
   agent-venv\Scripts\activate
   # For macOS/Linux
   source agent-venv/bin/activate
   
   # Install required packages
   pip install google-generativeai google-adk vertexai google-cloud-aiplatform python-dotenv
   ```

3. **Configuration**:
   * Create a `.env` file with your Google Cloud credentials:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-name
   GOOGLE_CLOUD_LOCATION=your-preferred-region
   GOOGLE_CLOUD_STORAGE_BUCKET=your-storage-bucket
   ```
   * Authenticate your GCloud account:
   ```bash
   gcloud auth application-default login
   ```

## Running the Agent

* **Option 1**: Run with the ADK CLI:
  ```bash
  adk run mikoko_guardian
  ```

* **Option 2**: Use the web interface:
  ```bash
  cd mikoko_guardian
  adk web
  ```
  Then navigate to the URL displayed in your terminal to interact with the agent.

## Deployment

To deploy the agent to Google Cloud:

1. Build the package:
   ```bash
   python -m build
   ```

2. Run the deployment script:
   ```bash
   python -m mikoko_guardian.deployment.deploy
   ```

3. To delete the deployed agent:
   ```bash
   python mikoko_guardian/deployment/deploy.py --delete --resource_id=${AGENT_ENGINE_ID}
   ```

## Customization

This agent sample focuses on mangrove conservation in Kenya but can be extended to other regions or environmental conservation domains:

1. Modify the species and site data in `agent.py` to include additional regions or species.
2. Adjust carbon calculation parameters based on regional research data.
3. Extend the restoration planning function with additional site-specific considerations.

## Troubleshooting

* **Q1**: I'm seeing authentication errors when trying to deploy the agent.
  * **A1**: Ensure you've run `gcloud auth application-default login` and set up your `.env` file with the correct project ID, location, and bucket name.

* **Q2**: The agent isn't providing information about a specific mangrove site I'm interested in.
  * **A2**: The agent currently contains data for five major mangrove sites in Kenya. You can extend the `KENYA_COASTAL_REGIONS` dictionary in `agent.py` to include additional sites.

## Acknowledgement

The Mikoko Guardian agent is designed to support mangrove conservation efforts in Kenya. "Mikoko" is the Swahili word for mangroves, highlighting the project's focus on local knowledge and ecosystems.