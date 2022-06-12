>PROJECT_ID='tactile-rigging-352016'
>IMAGE_URI="gcr.io/$PROJECT_ID/dataset-melanoma:v1"
>docker build ./ -t $IMAGE_URI
>docker push $IMAGE_URI
