PATH=%env PATH
%env PATH={PATH}:/home/jupyter/.local/bin
REGION="europe-west1"

# Get projet name
shell_output=!gcloud config get-value project 2> /dev/null
PROJECT_ID=shell_output[0]

# Set bucket name
BUCKET_NAME="gs://"+PROJECT_ID+"-bucket-winequality"

# Create bucket
PIPELINE_ROOT = f"{BUCKET_NAME}/pipeline_root_wine/"
PIPELINE_ROOT

USER_FLAG = "--user"
#!gcloud auth login if needed