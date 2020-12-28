# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eztrace(AutotoolsPackage):
    """EZTrace is a tool to automatically generate execution traces
       of HPC applications."""

    homepage = "http://eztrace.gforge.inria.fr"
    url      = "https://gitlab.com/eztrace/eztrace/-/archive/eztrace-1.1-10/eztrace-eztrace-1.1-10.tar.gz"
    maintainers = ['trahay']

    version('1.1-10', sha256='97aba8f3b3b71e8e2f7ef47e00c262234e27b9cb4a870c85c525317a83a3f0d4')

    depends_on('mpi')

    # Does not work on Darwin due to MAP_POPULATE
    conflicts('platform=darwin')

    def patch(self):
        filter_file(
            '"DEFAULT_OUTFILE"',
            '" DEFAULT_OUTFILE "',
            'extlib/gtg/extlib/otf/tools/otfshrink/otfshrink.cpp',
            string=True
        )

    def setup_build_environment(self, env):
        if self.spec.satisfies('%fj'):
            env.set('LDFLAGS', '--linkfortran')

    def configure_args(self):
        args = ["--with-mpi={0}".format(self.spec["mpi"].prefix)]
        return args

    @run_before('build')
    def fix_libtool(self):
        if self.spec.satisfies('%fj'):
            libtools = ['extlib/gtg/libtool',
                        'extlib/opari2/build-frontend/libtool']
            for f in libtools:
                filter_file('wl=""', 'wl="-Wl,"', f, string=True)
