# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#!/bin/bash

set -e

# this script was designed after this commit to a gitlab-runner fork (MIT)
# https://gitlab.com/outschool-eng/gitlab-runner/-/commit/65d5c4d468ffdbde0ceeafd9168d1326bae8e708
# we rely upon the ability to view kernel messages in the build container

# exit early if job was successful or not on AWS
[[ "$CI_JOB_STATUS" != "failed" ]] && exit 0
[[ "$CI_RUNNER_TAGS" != *"aws"* ]] && exit 0

# ensure /proc/1/cgroup exists
if [[ ! -f /proc/1/cgroup ]]; then
  echo "Error: /proc/1/cgroup not found"
  exit 1
fi

# Look for an OOM kill in the build container cpuset or any other container with the pod level memory in path
# the dmesg line will look like:
# [ 1578.430541] oom-kill:constraint=CONSTRAINT_MEMCG,nodemask=(null),cpuset=657a5777a8dbad52481bde927e9464ce5a838ad75f14ddf4322a32104786bce2,mems_allowed=0,oom_memcg=/kubepods/burstable/pod53bff6f9-f52d-418b-abf1-b5df128eb9cd/657a5777a8dbad52481bde927e9464ce5a838ad75f14ddf4322a32104786bce2,task_memcg=/kubepods/burstable/pod53bff6f9-f52d-418b-abf1-b5df128eb9cd/657a5777a8dbad52481bde927e9464ce5a838ad75f14ddf4322a32104786bce2,task=sh,pid=30361,uid=0
# where the last chunk of cgroup would be 657a5777a8dbad52481bde927e9464ce5a838ad75f14ddf4322a32104786bce2
# and the pod level memory config dir would be pod53bff6f9-f52d-418b-abf1-b5df128eb9cd, sourced from the second to last chunk
# we are not interfering with other processes on the same node, as the runner is in a container
# and we are filtering by the pod/container-level cgroup identifier in the dmesg output

proc1_cgroup=$(cat /proc/1/cgroup)
ctr_cgroup=$(echo "$proc1_cgroup" | tr / '\n' | tail -1 | tr -d '[:space:]')
pod_cgroup=$(echo "$proc1_cgroup" | tr / '\n' | tail -2 | head -1 | tr -d '[:space:]')
dmesg_out=$(dmesg)

OOM_MESSAGE="This job was killed due to memory constraints. Report to #ci-and-pipelines in Slack if you need help."
SPACK_ARTIFACTS_ROOT=${CI_PROJECT_DIR}/jobs_scratch_dir
JOB_INFO="${SPACK_ARTIFACTS_ROOT}/logs/job_metadata.txt"

mkdir -p ${SPACK_ARTIFACTS_ROOT}/logs

if echo "$dmesg_out" | grep -q "oom-kill.*$ctr_cgroup"; then
  echo $OOM_MESSAGE
  echo "OOM: container" >> $JOB_INFO
elif echo "$dmesg_out" | grep -q "oom-kill.*$pod_cgroup"; then
  echo $OOM_MESSAGE
  echo "OOM: pod" >> $JOB_INFO
fi
