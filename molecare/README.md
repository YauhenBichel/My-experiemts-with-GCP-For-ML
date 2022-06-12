## Build the container

>PROJECT_ID='tactile-rigging-352016'
>IMAGE_URI="gcr.io/$PROJECT_ID/melanoma-or-not:hypertune"

Configure docker
>gcloud auth configure-docker

Build the container by running the following from the root of your melanona_or_not directory:
>docker build ./ -t $IMAGE_URI

Push it to Google Container Registry:
>docker push $IMAGE_URI


https://www.tensorflow.org/datasets/gcs 
Create a GCS bucket and ensure you (or your service account) have read/write permissions on it (see authorization instructions above)

When you use tfds, you can set data_dir to "gs://YOUR_BUCKET_NAME"
ds_train, ds_test = tfds.load(name="mnist", split=["train", "test"], data_dir="gs://YOUR_BUCKET_NAME")


