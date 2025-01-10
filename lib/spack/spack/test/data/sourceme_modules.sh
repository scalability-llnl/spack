#!/usr/bin/env bash
#
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

_module_raw() { return 1; };
module() { return 1; };
ml() { return 1; };
export -f _module_raw;
export -f module;
export -f ml;

export MODULES_AUTO_HANDLING=1
export __MODULES_LMCONFLICT=bar&foo
export NEW_VAR=new
