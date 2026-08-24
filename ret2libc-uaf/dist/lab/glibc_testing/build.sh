#!/usr/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <distro> <image_name>"
    echo "Example: $0 debian:sid glibc_2.40"
    echo "Check "libc2distro.map" to see the libc to distro mapping."
    exit 1
fi

DISTRO=${1}
IMAGE_NAME=${2}

docker build \
  --build-arg BASE_IMAGE=$DISTRO \
  -t $IMAGE_NAME .
