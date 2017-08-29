FROM gcr.io/cloud-datalab/datalab:local

# Install the protocol buffer compiler so we can compile protocol buffers
RUN apt-get update -y && \
    apt-get install -y g++ make && \
    wget -O /tmp/protobuf-python-3.4.0.tar.gz \
    https://github.com/google/protobuf/releases/download/v3.4.0/protobuf-python-3.4.0.tar.gz && \
    tar -C /tmp -xvf /tmp/protobuf-python-3.4.0.tar.gz && \
    cd /tmp/protobuf-3.4.0 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    rm -rf /tmp/protobuf-python-3.4.0

# /usr/local/lib isn't on the linker path so protoc has problems finding the protoc.so.
env LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

RUN gcloud components install --quiet kubectl

RUN python -m pip install grpcio grpcio-tools
