#!/usr/bin/env bash
#
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)



if [[ "$1" == "intel64" ]] ; then
    export FOO='intel64'
else
    export FOO='default'
fi
