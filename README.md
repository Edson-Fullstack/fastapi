## Google Cloud Run + fastapi

Quick and dirty experiment with GCR + fastapi demo

Definitely not production ready.

Example commands to run the test service
```shell
$ gcloud auth configure-docker
$ docker build -t gcr.io/almostproductive/hello-run .
$ docker push gcr.io/almostproductive/hello-run
$ gcloud run deploy --image gcr.io/almostproductive/hello-run --platform managed
```