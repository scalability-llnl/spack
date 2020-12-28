# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libctl(AutotoolsPackage):
    """libctl is a free Guile-based library implementing flexible
    control files for scientific simulations."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/Libctl"
    url      = "http://ab-initio.mit.edu/libctl/libctl-3.2.2.tar.gz"
    list_url = "http://ab-initio.mit.edu/libctl/old"

    version('3.2.2', sha256='8abd8b58bc60e84e16d25b56f71020e0cb24d75b28bc5db86d50028197c7efbc')

    depends_on('guile')

    def configure_args(self):
        spec = self.spec

        return [
            '--enable-shared',
            'GUILE={0}'.format(join_path(
                spec['guile'].prefix.bin, 'guile')),
            'GUILE_CONFIG={0}'.format(join_path(
                spec['guile'].prefix.bin, 'guile-config')),
        ]
