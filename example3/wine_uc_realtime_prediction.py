ENDPOINT_NAME="winequality_endpoint"
instance = [[1,2,3,2,1,2,3,6,7,10]]
ENDPOINT_ID = !(gcloud ai endpoints list --region=$REGION \
              --format='value(ENDPOINT_ID)'\
              --filter=display_name=$ENDPOINT_NAME \
              --sort-by=creationTimeStamp | tail -1)
ENDPOINT_ID = ENDPOINT_ID[1]

def endpoint_predict(
    project: str, location: str, instances: list, endpoint: str
):
    aiplatform.init(project=project, location=location)

    endpoint = aiplatform.Endpoint(endpoint)

    prediction = endpoint.predict(instances=instances)
    return prediction

endpoint_predict(PROJECT_ID, REGION, instance, ENDPOINT_ID)