FROM mambaorg/micromamba:0.23.0
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /tmp/env.yaml
RUN micromamba install -y -f /tmp/env.yaml && \
    micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR /home/mambauser
RUN git clone https://github.com/AEP50/chandra-bot chandra_bot
RUN python -m pip install -e ./chandra_bot
