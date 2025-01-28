#!/bin/bash -e
git config --global user.email "spack@example.com"
git config --global user.name "Test User"

# create a local pr base branch
if [[ -n $GITHUB_BASE_REF ]]; then
    git fetch origin "${GITHUB_BASE_REF}:${GITHUB_BASE_REF}"
fi
