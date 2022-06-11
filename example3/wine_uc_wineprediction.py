# Define variables 
job_display_name = "winequality-batch-prediction-job"
MODEL_NAME="winequality"
ENDPOINT_NAME="winequality_endpoint"
BUCKET_URI="gs://your-bucket-winequality/pipeline_root_wine/332188XXXX/pipeline-winequality-20211227155508/get-wine-data_8271177375014715392"
input_file_name="test.csv"

# Get model id
MODEL_ID=!(gcloud ai models list --region=$REGION \
           --filter=display_name=$MODEL_NAME)
MODEL_ID=MODEL_ID[2].split(" ")[0]

model_resource_name = f'projects/{PROJECT_ID}/locations/{REGION}/models/{MODEL_ID}'
gcs_source= [f"{BUCKET_URI}/{input_file_name}"]
gcs_destination_prefix=f"{BUCKET_URI}/output"

def batch_prediction_job(
    project: str,
    location: str,
    model_resource_name: str,
    job_display_name: str,
    gcs_source: str,
    gcs_destination_prefix: str,
    machine_type: str,
    starting_replica_count: int = 1, # The number of nodes for this batch prediction job. 
    max_replica_count: int = 1,    
):   
    aiplatform.init(project=project, location=location)

    model = aiplatform.Model(model_resource_name)

    batch_prediction_job = model.batch_predict(
        job_display_name=job_display_name,
        instances_format='csv', #json
        gcs_source=[f"{BUCKET_URI}/{input_file_name}"],
        gcs_destination_prefix=f"{BUCKET_URI}/output",
        machine_type=machine_type, # must be present      
    )
    batch_prediction_job.wait()
    print(batch_prediction_job.display_name)
    print(batch_prediction_job.state)
    return batch_prediction_job

batch_prediction_job(PROJECT_ID, REGION, model_resource_name, job_display_name, gcs_source, gcs_destination_prefix, machine_type="n1-standard-2")
