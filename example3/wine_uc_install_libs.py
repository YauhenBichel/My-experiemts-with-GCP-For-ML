USER_FLAG = "--user"
# Install ai platform and kfp
!pip3 install {USER_FLAG} google-cloud-aiplatform==1.3.0 --upgrade
!pip3 install {USER_FLAG} kfp --upgrade
!pip install google_cloud_pipeline_components

!gcloud services enable compute.googleapis.com         \
                       containerregistry.googleapis.com  \
                       aiplatform.googleapis.com  \
                       cloudbuild.googleapis.com \
                       cloudfunctions.googleapis.com