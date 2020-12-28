# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libksba(AutotoolsPackage):
    """Libksba is a library to make the tasks of working with X.509
       certificates, CMS data and related objects more easy. """

    homepage = "https://gnupg.org/software/libksba/index.html"
    url = "https://gnupg.org/ftp/gcrypt/libksba/libksba-1.3.5.tar.bz2"

    version('1.4.0', sha256='bfe6a8e91ff0f54d8a329514db406667000cb207238eded49b599761bfca41b6')
    version('1.3.5', sha256='41444fd7a6ff73a79ad9728f985e71c9ba8cd3e5e53358e70d5f066d35c1a340')

    depends_on('libgpg-error@1.8:')

    conflicts('%apple-clang@12:', when='@:1.3')

    def configure_args(self):
        return [
            '--with-libgpg-error-prefix=' + self.spec['libgpg-error'].prefix
        ]
