ARG BASE_IMAGE=ubuntu:22.04
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        gcc \
        g++ \
        make \
        gdb \
        libc6-dev \
        file \
        wget \
        vim \
        python3 \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /work
CMD ["/bin/bash"]
