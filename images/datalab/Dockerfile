FROM gcr.io/cloud-datalab/datalab:local

# Install the protocol buffer compiler so we can compile protocol buffers
RUN apt-get update -y && \
    apt-get install -y g++ make && \
    wget -O /tmp/protobuf-python-3.4.0.tar.gz \
    https://github.com/google/protobuf/releases/download/v3.4.0/protobuf-python-3.4.0.tar.gz && \
    tar -xvf -C /tmp /tmp/protobuf-python-3.4.0.tar.gz && \
    cd /tmp/protobuf-python-3.4.0 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    rm -rf /tmp/protobuf-python-3.4.0