#!/usr/bin/env bash
#
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# split the package index in a small file tree of
#    /p/package.json
# files with sub-directories grouped by the initial letter of the packages

base_dir=$(pwd)/packages/

for pkg in $(cat packages.json | jq -c '.[]')
do
    name="$(echo ${pkg} | jq -r '.name')";
    first_letter=${name::1}
    mkdir -p ${base_dir}${first_letter}/
    echo ${pkg} > ${base_dir}${first_letter}/${name}.json
done
