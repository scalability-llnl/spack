# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcyaml(MakefilePackage):
    """LibCYAML is a C library for reading and writing structured YAML
    documents. It is written in ISO C11 and licensed under the ISC licence."""

    homepage = "https://github.com/tlsa/libcyaml"
    url      = "https://github.com/tlsa/libcyaml/archive/v1.1.0.tar.gz"

    version('1.1.0', sha256='37a00ed8ec206b60a712acfd44196bef063b8f02e376d8e86f61a7007a81daea')

    depends_on('libyaml')

    def build(self, spec, prefix):
        make('VARIANT=release')

    def install(self, spec, prefix):
        make('install', 'VARIANT=release', 'PREFIX={0}'.format(prefix))
