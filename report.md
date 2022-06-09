https://medium.com/@piyushpandey282/model-serving-at-scale-with-vertex-ai-custom-container-deployment-with-pre-and-post-processing-12ac62f4ce76 

1. Dockerfile
- FROM tensorflow/tensorflow:nightly-gpu : This is the first command of Dockerfile and tensorflow/tensorflow:nightly-gpu is the base image that is required because here we have assumed that our application runs on tensorflow in backend. Tensorflow is installed on top of small linux like alpine. Here I have used gpu based tensorflow image. You can find more such images on docker hub. It is important to note that GPU based images are version specific and installs cuda and cudnn respectively. Each tensorflow version is compatible with a specific cuda version. You can find more here on their compatibility. If you don’t intend to use gpu for your project, use the cpu image. Find more on tensorflow images here .
- WORKDIR /app : To specify the working directory.
- COPY . /app : Copy all the contents mentioned in the application content image above to app directory.
- RUN pip install — trusted-host pypi.python.org -r requirements.txt : RUN helps us execute any linux command, and any RUN command gets executed inside the container. We will install everything that is needed for our application to run using requirements.txt.
- CMD gunicorn — bind 0.0.0.0:5005 — timeout=150 app:app -w 5: CMD is an entry point command. There can be only one CMD command and it is the first command to get executed when a container is run. Hence in this case app.py will get executed first. I am binding the local host with 5005 port of container using gunicorn and have exposed the same port, this way we can specify on which port the container will listen. It is not advised to use a flask server for production, hence I am using gunicorn server on top of flask. We then specify the name of the flask app that we want to run, in our case app. At last we specify how many workers we want, in my case I wanted 5 workers, by default its 1 worker. I have also specified the timeout of worker to be 150 sec, if you don’t specify timeout it will considered as 30 sec by default.

2. build.txt
This created a custom docker image on my local machine with the specified image tag name. $PROEJCT_ID and $REGION are the placeholders for the names of my GCP project id and region. $REPOSITORY and $IMAGE are the names given to my artifact registry repository and docker image for the custom container.

3. run.txt
Test Custom Container Locally
Here I have mapped 5005 port of local host with 5005 port of container for serving HTTP request. In my case I am going to use gpu, hence I have used gpus=all in run command.

After the container is running, use the below command to send request to the server.
>curl -X POST -d "@sample_input.json" -H "Content-Type: application/json" http://localhost:5005/predict

4. sample_input.json
The sample_input.json file contains json request which is modified according to the vertex ai request format. Note that all of the model input data fields need to be wrapped by a top-level element “instances” in an array. This data structure is required by Vertex AI in the custom container implementation. I have adjusted my code in predict() function of app.py as well to accomodate that change.

The custom container is expected to return a HTTP response with a JSON content of the prediction values . This confirms that the docker image is built correctly and the custom container is working appropriately in the local environment.

5. Deploy Custom Container to Vertex AI
After local testing, the custom container can now be deployed to Vertex AI. At first, I created an Artifact Registry repository on GCP and pushed the docker image to this repository. Make sure you have all the required permissions for artifact registry and Vertex AI. A quick google search will tell you what you require.

>gcloud beta artifacts repositories create $REPOSITORY \
 --repository-format=docker \
 --location=$REGION

 >docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE

6. Then, I imported a custom model on Vertex AI using the docker image pushed in the artifact repository. Specify the model name in $MODEL_NAME placeholder.

>gcloud beta ai models upload \
  --region=$REGION \
  --display-name=$MODEL_NAME \
  --container-image-uri=$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE \
  --container-ports=5005 \
  --container-health-route=/healthz \
  --container-predict-route=/predict

Note that in the above command, the container port is specified as 5005 and the health check and prediction routes are also specified based on their definitions in the Flask web server code. Once the model import is completed, it can be confirmed by navigating to Vertex AI console or running the following command:

>gcloud beta ai models list \
  --region=$REGION \
  --filter=display_name=$MODEL_NAME

7. Finally, I created an endpoint and deployed the custom model to the endpoint for serving. Specify endpoint name in $ENDPOINT_NAME placeholder.

>gcloud beta ai endpoints create \
  --region=$REGION \
  --display-name=$ENDPOINT_NAME

Now upload the model to endpoint. Make sure you provide correct model id and endpoint id. You can see the model id and endpoint ids by running the above two commands or in the Vertex AI console.

>#if you don't want gpu's
gcloud beta ai endpoints deploy-model $ENDPOINT_ID \
  --region=$REGION \
  --model=$MODEL_ID \
  --display-name=$DEPLOYED_MODEL_NAME \
  --machine-type=n1-standard-4 \
  --min-replica-count=1 \
  --max-replica-count=2 \
  --traffic-split=0=100
  
  #if you want gpus
  >gcloud beta ai endpoints deploy-model $ENDPOINT_ID \
  --region=$REGION \
  --model=$MODEL_ID \
  --display-name=$DEPLOYED_MODEL_NAME \
  --machine-type=n1-standard-4 \
  --accelerator=count=1,type=nvidia-tesla-t4 \
  --min-replica-count=1 \
  --max-replica-count=2 \
  --traffic-split=0=100

where $ENDPOINT_ID is the endpoint id assigned by Vertex AI after the endpoint was created. Here I specified that each node of the cluster uses the standard 4-vCPU machine type, 1 nvidia-tesla GPU and the minimum number of nodes is 1 and the maximum number is 2(auto-scaled from1 to 2). This step might take around 20–30 minutes to complete, so be patient.

After some time we can see the deployed model at our endpoint in Vertex AI UI.

8. Testing the custom container on Vertex AI
After the custom container was deployed, I ran the following tests to ensure that the endpoint works correctly:

There are two important things to note here. First is that the above code is giving desired output, second is that the url and the token that is generated will be used for authorization in postman and load test using jmeter.

9. Summary
Custom container deployment in Vertex AI is very flexible and helps to scale our model without having to worry about the cluster management. It efficiently autoscales our model when we receive high traffic and is a good choice for model serving.





