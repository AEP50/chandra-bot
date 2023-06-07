FROM mcr.microsoft.com/vscode/devcontainers/anaconda

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      protobuf-compiler

COPY environment-old-mac.yml /tmp/conda-tmp/
RUN /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment-old-mac.yml

# RUN protoc -I=./chandra_bot --python_out=./chandra_bot ./chandra_bot/data_model.proto
# RUN pip install -e .
