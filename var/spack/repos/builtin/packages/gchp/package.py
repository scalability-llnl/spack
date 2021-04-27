# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil


class Gchp(CMakePackage):
    """GEOS-Chem High Performance model of atmospheric chemistry"""

    homepage = "https://gchp.readthedocs.io/"
    url      = "https://github.com/geoschem/GCHP/archive/13.0.1.tar.gz"

    maintainers = ['williamdowns']

    version('13.0.1', git='https://github.com/geoschem/GCHP.git',
            commit='f40a2476fda901eacf78c0972fdb6c20e5a06700',  submodules=True)
    version('13.0.0', git='https://github.com/geoschem/GCHP.git',
            commit='1f5a5c5630c5d066ff8306cbb8b83e267ca7c265',  submodules=True)

    patch('for_aarch64.patch', when='target=aarch64:')

    depends_on('esmf@8.0.1', when='@13.0.0:')
    depends_on('esmf@8.0.1: -lapack -pio -pnetcdf -xerces', when='@13.0.0-rc.0')
    depends_on('mpi@3')
    depends_on('netcdf-fortran')
    depends_on('cmake@3.13:')
    depends_on('libfabric', when='+ofi')
    depends_on('m4')

    variant('omp',   default=False, description="OpenMP parallelization")
    variant('real8', default=True,  description="REAL*8 precision")
    variant('apm',   default=False, description="APM Microphysics (Experimental)")
    variant('rrtmg', default=False, description="RRTMG radiative transfer model")
    variant('luo',   default=False, description="Luo et al 2019 wet deposition scheme")
    variant('tomas', default=False, description="TOMAS Microphysics (Experimental)")
    variant('ofi',   default=False, description="Build with Libfabric support")

    def cmake_args(self):
        args = [self.define("RUNDIR", self.prefix),
                self.define_from_variant('OMP', 'omp'),
                self.define_from_variant('USE_REAL8', 'real8'),
                self.define_from_variant('APM', 'apm'),
                self.define_from_variant('RRTMG', 'rrtmg'),
                self.define_from_variant('LUO_WETDEP', 'luo'),
                self.define_from_variant('TOMAS', 'tomas')]
        return args

    def install(self, spec, prefix):
        super().install(spec, prefix)
        # Preserve source code in prefix for two reasons:
        # 1. Run directory creation occurs independently of code compilation,
        # possibly multiple times depending on user needs,
        # and requires the preservation of some of the source code structure.
        # 2. Run configuration is relatively complex and can result in error
        # messages that point to specific modules / lines of the source code.
        # Including source code thus facilitates runtime debugging.
        shutil.move(self.stage.source_path,
                    join_path(prefix, 'source_code'))
