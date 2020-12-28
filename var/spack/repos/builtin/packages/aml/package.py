# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aml(AutotoolsPackage):
    """AML: Building Blocks for Memory Management."""

    homepage = "https://xgitlab.cels.anl.gov/argo/aml"
    url = "https://www.mcs.anl.gov/research/projects/argo/downloads/aml-0.1.0.tar.gz"
    git = "https://xgitlab.cels.anl.gov/argo/aml.git"
    version('0.1.0', sha256='cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b')
    version('develop', branch='staging')
    version('master', branch='master')

    depends_on('numactl')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
