# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Clinfo(MakefilePackage):
    """Print all known information about all available OpenCL platforms and
    devices in the system."""

    homepage = "https://github.com/Oblomov/clinfo"
    url      = "https://github.com/Oblomov/clinfo/archive/2.2.18.04.06.tar.gz"

    maintainers = ['matthiasdiener']

    version('2.2.18.04.06', sha256='f77021a57b3afcdebc73107e2254b95780026a9df9aa4f8db6aff11c03f0ec6c')

    depends_on('opencl')

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
