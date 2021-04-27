# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Geopm(AutotoolsPackage):
    """GEOPM is an extensible power management framework targeting HPC.
    The GEOPM package provides libgeopm, libgeopmpolicy and applications
    geopmctl and geopmpolicy, as well as tools for postprocessing.
    GEOPM is designed to be extended for new control algorithms and new
    hardware power management features via its plugin infrastructure.

    Note: GEOPM interfaces with hardware using Model Specific Registers (MSRs).
    For propper usage make sure MSRs are made available directly or via the
    msr-safe kernel module by your administrator."""

    homepage = "https://geopm.github.io"
    url      = "https://github.com/geopm/geopm/releases/download/v1.0.0/geopm-1.0.0.tar.gz"
    git      = "https://github.com/geopm/geopm.git"

    # Add additional proper versions and checksums here. "spack checksum geopm"
    version('develop', branch='dev')
    version('master', branch='master')
    version('1.1.0', sha256='5f9a4df37ef0d64c53d64829d46736803c9fe614afd8d2c70fe7a5ebea09f88e')
    version('1.0.0', sha256='24fe72265a7e44d62bdfe49467c49f0b7a649131ddda402d763c00a49765e1cb')
    version('0.6.1', sha256='0ca42853f90885bf213df190c3462b8675c143cc843aee0d8b8a0e30802b55a9')
    version('0.6.0', sha256='95ccf256c2b7cb35838978152479569d154347c3065af1639ed17be1399182d3')
    version('0.5.1', sha256='db247af55f7000b6e4628af099956349b68a637500b9d4fe8d8fb13687124d53')
    version('0.5.0', sha256='cdc123ea68b6d918dcc578a39a7a38275a5d711104364eb889abed15029f4060')
    version('0.4.0', sha256='7d165f5a5fe0f19ca586bd81a4631202effb542e9d762cc9cc86ad6ef7afcad9')
    version('0.3.0', sha256='73b45d36e7d2431d308038fc8c50a521a1d214c5ce105a17fba440f28509d907')

    # Variants reflecting most ./configure --help options
    variant('debug', default=False, description='Enable debug.')
    variant('coverage', default=False, description='Enable test coverage support, enables debug by default.')
    variant('overhead', default=False, description='Enable GEOPM to calculate and display time spent in GEOPM API calls.')
    variant('procfs', default=True, description='Enable procfs (disable for OSes not using procfs).')
    variant('mpi', default=True, description='Enable MPI dependent components.')
    variant('fortran', default=True, description='Build fortran interface.')
    variant('doc', default=True, description='Create man pages with ruby-ronn.')
    variant('openmp', default=True, description='Build with OpenMP.')
    variant('ompt', default=False, description='Use OpenMP Tools Interface.')
    variant('gnu-ld', default=False, description='Assume C compiler uses gnu-ld.')

    # Added dependencies.
    depends_on('ruby-ronn', type='build', when='+doc')
    depends_on('doxygen', type='build', when='+doc')
    depends_on('mpi@2.2:', when='+mpi')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('ruby-ronn', type='build', when='+doc')
    depends_on('doxygen', type='build', when='+doc')
    depends_on('numactl', when="@:1.0.0-rc2")
    depends_on('mpi', when='+mpi')
    depends_on('hwloc@1.11.9', when='@:0.5.1')
    depends_on('json-c', when='@:0.9.9')
    depends_on('py-cycler@0.10.0:', when="@1.0.0:", type=('build', 'run'))
    depends_on('py-pandas@0.22.0:', type=('build', 'run'))
    depends_on('py-tables@3.4.3:3.5.2', when="@1.0.0:", type=('build', 'run'))
    depends_on('py-cffi@1.6.0:', when="@1.1.0:", type=('build', 'run'))
    depends_on('py-pyyaml@5.1.0:', when="@1.1.0:", type=('build', 'run'))
    depends_on('py-mock@3.0.0:', when="@1.1.0:", type=('build', 'run'))
    depends_on('py-future@0.17.1:', when="@1.1.0:", type=('build', 'run'))
    depends_on('py-numpy@1.14.3:', type=('build', 'run'))
    depends_on('py-setuptools@39.2.0:', when="@1.0.0:", type='build')
    depends_on('py-natsort@5.3.2:', type=('build', 'run'))
    depends_on('py-psutil@5.4.8:', when="@1.0.0:", type=('build', 'run'))
    depends_on('py-pylint@1.9.5:', when="@1.1.0:", type=('build', 'run'))
    depends_on('py-matplotlib@2.2.3', when="@:1.0.0-rc2", type=('build', 'run'))
    depends_on('py-matplotlib@2.2.3:', when="@1.1.0:", type=('build', 'run'))

    parallel = False

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash('./autogen.sh')

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable('debug'))
        args.extend(self.enable_or_disable('coverage'))
        args.extend(self.enable_or_disable('overhead'))
        args.extend(self.enable_or_disable('procfs'))
        args.extend(self.enable_or_disable('mpi'))
        args.extend(self.enable_or_disable('fortran'))
        args.extend(self.enable_or_disable('doc'))
        args.extend(self.enable_or_disable('openmp'))
        args.extend(self.enable_or_disable('ompt'))
        args.extend(self.with_or_without('gnu-ld'))

        return args
