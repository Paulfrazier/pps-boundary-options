#!/bin/bash
# Build OSRM MLD graphs. Usage: run_build.sh foot|bicycle   (dir: foot|bike)
set -e
cd "$(dirname "$0")"
PROF=$1; DIR=$2
for step in "osrm-extract -p /opt/$PROF.lua /data/map.osm.pbf" "osrm-partition /data/map.osrm" "osrm-customize /data/map.osrm"; do
 docker run --rm -v "$PWD/$DIR:/data" osrm/osrm-backend $step
done
echo BUILD_DONE
