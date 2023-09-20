# Image API

## Installing dependencies

```
cd imageapi
poetry install
```

## Running it locally

```
cd imageapi
poetry run python app.py
```

## TODO

- Find out how to make the app.py listen to all interfaces
- Pick a unique port between 5000 and 6000 (I've opened the firewall for those)
- Make your app accessible from the web
- Modify test.py to point to your API, and check whether it works.

# Deploying to Cloud Run 

- Restore the default settings for binding and port
- Run the following commands to deploy the application to GCP Cloud Run
- Verify your application works by modifying test.py and running test.py
  against your Cloud Run URL

Docker commands:

```
docker buildx build . --platform linux/amd64 -t imageapi
docker tag imageapi gcr.io/xebia-ai-training/yourname-imageapi
docker push gcr.io/xebia-ai-training/yourname-imageapi
gcloud run deploy yourname-imageapi \
  --image gcr.io/xebia-ai-training/yourname-imageapi \
  --platform managed --region us-east1 --allow-unauthenticated
```
