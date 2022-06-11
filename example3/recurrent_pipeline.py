from kfp.v2.google.client import AIPlatformClient

api_client = AIPlatformClient(
                project_id=PROJECT_ID,
                region=REGION,
                )

SERVICE_ACCOUNT = (
    "XXXXXX@developer.gserviceaccount.com" # Replace the Xs with your generated service-account.
)
response = api_client.create_schedule_from_job_spec(
    enable_caching=True,
    job_spec_path="ml_winequality.json",
    schedule="0 0 * * 1", //once per week on Monday
    time_zone="Europe/Brussels",  # change this as necessary
    parameter_values={"display_name": DISPLAY_NAME},
    pipeline_root=PIPELINE_ROOT,  
    service_account=SERVICE_ACCOUNT,    
)