# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

###############################################################################
#
# This file is part of Spack and sets up the environment for the Spack tutorial
# It is intended to be run on ubuntu-18.04 or an ubuntu-18.04 container or AWS
# cloud9 environment
#
# Components:
# 1. apt installs for packages used in the tutorial
#     these include compilers and externals used by the tutorial and
#     basic spack requirements like python and curl
# 2. spack configuration files
#     these set the default configuration for Spack to use x86_64 and suppress
#     certain gpg warnings. The gpg warnings are not relevant for the tutorial
#     and the default x86_64 architecture allows us to run the same tutorial on
#     any x86_64 architecture without needing new binary packages.
# 3. aws cloud9 configuration to expand available storage
#     when we run on aws cloud9 we have to expand the storage from 10G to 30G
#     because we install too much software for a default cloud9 instance
###############################################################################

####
# Ensure we're on Ubuntu 18.04
####

if [ -f /etc/os-release ]; then
    . /etc/os-release
fi
if [ x"$UBUNTU_CODENAME" != "xbionic" ]; then
    echo "The tutorial setup script must be run on Ubuntu 18.04."
    return 1 &>/dev/null || exit 1    # works if sourced or run
fi

####
# Install packages needed for tutorial
####

# compilers, basic system components, externals
# There are retries around these because apt fails frequently on new instances,
# due to unattended updates running in the background and taking the lock.
until sudo apt-get update -y; do
    echo "==> apt-get update failed. retrying..."
    sleep 5
done

until sudo apt-get install -y --no-install-recommends \
    autoconf make python3 python3-pip \
    build-essential ca-certificates curl git gnupg2 iproute2 emacs \
    file openssh-server tcl unzip vim wget \
    clang g++ g++-6 gcc gcc-6 gfortran gfortran-6 \
    zlib1g zlib1g-dev mpich; do
    echo "==> apt-get install failed. retrying..."
    sleep 5
done

####
# Upgrade boto3 python package on AWS systems
####
pip3 install --upgrade boto3


####
# Spack configuration settings for tutorial
####

# create spack system config
sudo mkdir -p /etc/spack

# set default arch to x86_64
sudo tee /etc/spack/packages.yaml << EOF > /dev/null
packages:
  all:
    target: [x86_64]
EOF

# suppress gpg warnings
sudo tee /etc/spack/config.yaml << EOF > /dev/null
config:
  suppress_gpg_warnings: true
EOF

####
# AWS set volume size to at least 30G
####

# Hardcode the specified size to 30G
SIZE=30

# Get the ID of the environment host Amazon EC2 instance.
INSTANCEID=$(curl http://169.254.169.254/latest/meta-data//instance-id)

# Get the ID of the Amazon EBS volume associated with the instance.
VOLUMEID=$(aws ec2 describe-instances \
           --instance-id $INSTANCEID \
           --query "Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId" \
           --output text)

# Resize the EBS volume.
aws ec2 modify-volume --volume-id $VOLUMEID --size $SIZE

# Wait for the resize to finish.
while [ \
      "$(aws ec2 describe-volumes-modifications \
    --volume-id $VOLUMEID \
    --filters Name=modification-state,Values="optimizing","completed" \
    --query "length(VolumesModifications)"\
    --output text)" != "1" ]; do
    sleep 1
done

if [ -e /dev/xvda1 ]
then
    # Rewrite the partition table so that the partition takes up all the space that it can.
    sudo growpart /dev/xvda 1

    # Expand the size of the file system.
    sudo resize2fs /dev/xvda1

else
    # Rewrite the partition table so that the partition takes up all the space that it can.
    sudo growpart /dev/nvme0n1 1

    # Expand the size of the file system.
    sudo resize2fs /dev/nvme0n1p1
fi
