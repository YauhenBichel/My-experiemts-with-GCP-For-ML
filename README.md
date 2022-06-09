Run the following command to create a source distribution, dist/trainer-0.1.tar.gz:

>python setup.py sdist --formats=gztar


# app.py
The above flask server contains two important functions that are required before deployment to Vertex AI.

predict() : It contains model prediction logic which is mapped to the predict route.
healthz(): Contains the health route. Vertex AI intermittently performs health checks on your HTTP server while it is running to ensure that it is ready to handle prediction requests. The service uses a health probe to send HTTP GET requests to a configurable health check path on your server.

Vertex AI has its own request and response format. We have to accept json requests in a specified format and send prediction response in a specified format.


