#!/usr/bin/env bash
#
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)



if [[ "$1" == "intel64" ]] ; then
    export FOO='intel64'
else
    export FOO='default'
fi
