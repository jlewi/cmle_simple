#!/bin/bash

PROJECT_NUMBER=236417448818
#SERVICE_ACCOUNT=cloud-ml-service-test@cml-236417448818-test.iam.gserviceaccount.com
SERVICE_ACCOUNT=cloud-ml-service@dataflow-jlewi-6880f.iam.gserviceaccount.com

BUCKET=dataflow-jlewi_cloud_ml
gsutil -m acl ch -u ${SERVICE_ACCOUNT}:W gs://${BUCKET}
gsutil -m defacl ch -u ${SERVICE_ACCOUNT}:R gs://${BUCKET}
gsutil -m acl ch -u ${SERVICE_ACCOUNT}:R -r gs://${BUCKET}