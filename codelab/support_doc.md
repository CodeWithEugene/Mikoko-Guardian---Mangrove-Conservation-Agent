# Set your Google Cloud Project ID
export GOOGLE_CLOUD_PROJECT="ng-workshop-lab"

# Set your desired Google Cloud Location
export GOOGLE_CLOUD_LOCATION="us-central1"

# Set the path to your agent code directory
export AGENT_PATH="./cv-focused" # Assuming capital_agent is in the current directory

# Set a name for your Cloud Run service (optional)
export SERVICE_NAME="cv-focused"

# Set an application name (optional)
export APP_NAME="cv-focused"

# Get your Google Cloud project number
gcloud projects describe $GOOGLE_CLOUD_PROJECT --format='value(projectNumber)'

# Grant the required role (replace [PROJECT_NUMBER] with the number):
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="serviceAccount:[PROJECT NUMBER]@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

export GOOGLE_CLOUD_PROJECT="ng-workshop-lab"
export GOOGLE_CLOUD_LOCATION="us-central1"
export AGENT_PATH="./cv-focused"
export SERVICE_NAME="cv-focused"
export APP_NAME="cv-focused"


adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--service_name=$SERVICE_NAME \
--app_name=$APP_NAME \
--with_ui \
$AGENT_PATH