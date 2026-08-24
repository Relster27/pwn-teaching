ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        gcc \
        libc6-dev \
        file \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY main.c .

RUN gcc main.c -o main -no-pie -g
RUN gcc main.c -o main-build -no-pie -g

# Copy out the exact loader and libc used by this distro
RUN cp /lib/x86_64-linux-gnu/libc.so.6 /work/ && \
    cp /lib64/ld-linux-x86-64.so.2 /work/ld.so

CMD ["/bin/bash"]
