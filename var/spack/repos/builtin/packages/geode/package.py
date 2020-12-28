# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geode(Package):
    """
    Apache Geode is a data management platform that provides real-time,
    consistent access to data-intensive applications throughout widely
    distributed cloud architectures.
    """

    homepage = "https://geode.apache.org/"
    url      = "https://archive.apache.org/dist/geode/1.9.2/apache-geode-1.9.2.tgz"

    version('1.9.2', sha256='4b8118114ef43166f6bf73af56b93aadbf9108fcab06d1fbbb8e27f7d559d7e0')
    version('1.9.0', sha256='8794808ebc89bc855f0b989b32e91e890d446cfd058e123f6ccb9e12597c1c4f')
    version('1.8.0', sha256='58edc41edac4eabd899322b73a24727eac41f6253274c2ce7d0a82227121ae3e')
    version('1.7.0', sha256='91eec04420f46e949d32104479c4a4b5b34a4e5570dca7b98ca067a30d5a783d')
    version('1.6.0', sha256='79e8d81d058b1c4edd5fb414ff30ac530f7913b978f5abc899c353fcb06e5ef3')

    depends_on('java', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
