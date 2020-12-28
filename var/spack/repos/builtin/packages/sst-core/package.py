# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstCore(AutotoolsPackage):
    """The Structural Simulation Toolkit (SST) core
       provides a parallel discrete event simulation (PDES)
       framework for performing architecture simulations
       of existing and proposed HPC systems"""

    homepage = "https://github.com/sstsimulator"
    git = "https://github.com/sstsimulator/sst-core.git"
    url = "https://github.com/sstsimulator/sst-core/releases/download/v10.0.0_Final/sstcore-10.0.0.tar.gz"

    maintainers = ['jjwilke']

    version('10.1.0', sha256="e464213a81c7b3ccec994fdba2b56992b52fb9a6db089ef7c3445b54306d4b87")
    version('10.0.0', sha256="64cf93a46dfab011fba49244bf0e0efe25ef928c6fbde1d49003220d0eb7735a")
    version('9.1.0',  sha256="cfeda39bb2ce9f32032480427517df62e852c0b3713797255e3b838075f3614d")
    version('develop', branch='devel')
    version('master',  branch='master')

    variant("pdes_mpi", default=True,
            description="Build support for parallel discrete event simulation")
    variant("zoltan",  default=False,
            description="Use Zoltan for partitioning parallel runs")
    variant("hdf5",    default=False,
            description="Build support for HDF5 statistic output")
    variant("zlib",    default=False,
            description="Build support for ZLIB compression")
    variant("preview", default=False,
            description="Preview build with deprecated features removed")

    depends_on("python", type=('build', 'run'))
    depends_on("mpi", when="+pdes_mpi")
    depends_on("zoltan", when="+zoltan")
    depends_on("hdf5", when="+hdf5")
    depends_on("zlib", when="+zlib")

    depends_on('autoconf@1.68:', type='build', when='@master:')
    depends_on('automake@1.11.1:', type='build', when='@master:')
    depends_on('libtool@1.2.4:', type='build', when='@master:')
    depends_on('m4', type='build', when='@master:')
    depends_on('gettext')

    # force out-of-source builds
    build_directory = 'spack-build'

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('autogen.sh')

    def configure_args(self):
        args = []
        if "+zoltan" in self.spec:
            args.append("--with-zoltan=%s" % self.spec["zoltan"].prefix)
        if "+hdf5" in self.spec:
            args.append("--with-hdf5=%s" % self.spec["hdf5"].prefix)
        if "+zlib" in self.spec:
            args.append("--with-zlib=%s" % self.spec["zlib"].prefix)

        if "+pdes_mpi" in self.spec:
            args.append("--enable-mpi")
            env['CC'] = self.spec['mpi'].mpicc
            env['CXX'] = self.spec['mpi'].mpicxx
            env['F77'] = self.spec['mpi'].mpif77
            env['FC'] = self.spec['mpi'].mpifc
        else:
            args.append("--disable-mpi")

        if "+preview" in self.spec:
            args.append("--enable-preview-build")

        args.append("--with-python=%s" % self.spec["python"].prefix)
        return args
