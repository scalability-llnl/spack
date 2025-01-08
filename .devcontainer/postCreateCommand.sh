#!/bin/bash

# Load spack environment at terminal startup
cat <<EOF >> /root/.bashrc
. /workspaces/spack/share/spack/setup-env.sh
EOF

# Load spack environment in this script
. /workspaces/spack/share/spack/setup-env.sh

# Ensure generic targets for maximum matching with buildcaches
spack config --scope site add "packages:all:require:[target=x86_64_v3]"
spack config --scope site add "concretizer:targets:granularity:generic"

# Find compiler and install gcc-runtime
spack compiler find --scope site

# Setup buildcaches
spack mirror add --scope site develop https://binaries.spack.io/develop
spack buildcache keys --install --trust
