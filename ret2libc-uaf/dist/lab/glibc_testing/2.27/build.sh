#!/usr/bin/bash
set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <distro> <glibc_version>"
    exit 1
fi

DISTRO=$1
VER=$2
IMAGE="glibc_builder_$VER"
OUTDIR="out_$VER"

docker build --build-arg BASE_IMAGE=$DISTRO -t $IMAGE .

CID=$(docker create $IMAGE)

mkdir -p $OUTDIR

docker cp $CID:/work/main $OUTDIR/
docker cp $CID:/work/main-build $OUTDIR/
docker cp $CID:/work/libc.so.6 $OUTDIR/
docker cp $CID:/work/ld.so $OUTDIR/

docker rm $CID

patchelf --set-interpreter ./ld.so $OUTDIR/main
patchelf --set-rpath . $OUTDIR/main

cat > $OUTDIR/run.sh << 'EOF'
#!/usr/bin/bash
DIR=$(dirname "$0")
LD_LIBRARY_PATH=$DIR $DIR/ld.so $DIR/main
EOF

chmod +x $OUTDIR/run.sh

echo "[+] Extracted to $OUTDIR"

cd $OUTDIR
