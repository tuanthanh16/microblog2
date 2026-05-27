# step 1. build a docker
docker build -t tuanthanh13/test-app .
# step 2. run /list docker image locally (from docker desktop) to verify
docker image ls
# step 3. copy google cloud repo link - "europe-west2-docker.pkg.dev/project-c3dab1ee-ee70-4c93-904/testapp-repo"
# authenticate 
# step 3. tag image to google clond artifact registry
docker tag tuanthanh13/test-app:latest europe-west2-docker.pkg.dev/project-c3dab1ee-ee70-4c93-904/testapp-repo/test-app:latest
# step 4. push image to google cloud repo
docker push europe-west2-docker.pkg.dev/project-c3dab1ee-ee70-4c93-904/testapp-repo/test-app:latest
# step 5. create google cloud run
# trong networking tab, input the port number, otherwise default = 8080
# google cloud CLI
gcloud -h
# authenticate docker
gcloud auth configure-docker europe-west2-docker.pkg.dev

# create bucket
# config set current project
gcloud config set project project-c3dab1ee-ee70-4c93-904
# Cloud region
# gcloud storage buckets create gs://<YOUR-BUCKET-NAME> --project=<YOUR-PROJECT-ID> --location=<YOUR-REGION>
gcloud storage buckets create gs://<YOUR-BUCKET-NAME> --project=<YOUR-PROJECT-ID> --location=<YOUR-REGION>