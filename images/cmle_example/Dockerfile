FROM python:2.7

RUN python -m pip install grpcio grpcio-tools http google-api-python-client google-cloud

COPY cmle_example-0.1.1.tar.gz /tmp/cmle_example-0.1.1.tar.gz
RUN pip install /tmp/cmle_example-0.1.1.tar.gz

# Install gcloud. This is primarily useful for logging in when running manually for testing.
RUN wget -O /tmp/google-cloud-sdk-168.0.0-linux-x86_64.tar.gz \
    https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-168.0.0-linux-x86_64.tar.gz  && \
    tar -C /tmp -xvf /tmp/google-cloud-sdk-168.0.0-linux-x86_64.tar.gz && \
    mv /tmp/google-cloud-sdk /usr/local && \
    /usr/local/google-cloud-sdk/install.sh --quiet && \
    rm /tmp/google-cloud-sdk-168.0.0-linux-x86_64.tar.gz
