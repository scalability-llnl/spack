# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstElements(AutotoolsPackage):
    """SST Elements implements a range of components for performing
       architecture simulation from node-level to system-level using
       the SST discrete event core
    """

    homepage = "https://github.com/sstsimulator"
    git = "https://github.com/sstsimulator/sst-elements.git"
    url = "https://github.com/sstsimulator/sst-elements/releases/download/v10.0.0_Final/sstelements-10.0.0.tar.gz"

    maintainers = ['jjwilke']

    version('10.1.0', sha256="a790561449795dac48a84c525b8e0b09f05d0b0bff1a0da1aa2e903279a03c4a")
    version('10.0.0', sha256="ecf28ef97b27ea75be7e64cb0acb99d36773a888c1b32ba16034c62174b02693")
    version('9.1.0', sha256="e19b05aa6e59728995fc059840c79e476ba866b67887ccde7eaf52a18a1f52ca")

    version('develop',   branch='devel')
    version('master',  branch='master')

    variant("pin",       default=False,
            description="Enable the Ariel CPU model")
    variant("dramsim2",  default=False,
            description="Build with DRAMSim2 support")
    variant("nvdimmsim", default=False,
            description="Build with NVDimmSim support")
    variant("hybridsim", default=False,
            description="Build with HybridSim support")
    variant("goblin",    default=False,
            description="Build with GoblinHMCSim support")
    variant("hbm",       default=False,
            description="Build with HBM DRAMSim2 support")
    variant("ramulator", default=False,
            description="Build with Ramulator support")

    depends_on("python", type=('build', 'run'))
    depends_on("sst-core")
    depends_on("sst-core@develop",  when="@develop")
    depends_on("sst-core@master", when="@master")

    depends_on("intel-pin",        when="+pin")
    depends_on("dramsim2@2:",      when="+dramsim2")
    depends_on("hybridsim@2.0.1",  when="+hybridsim")
    depends_on("nvdimmsim@2.0.0",  when="+nvdimmsim")
    depends_on("goblin-hmc-sim",   when="+goblin")
    depends_on("ramulator@sst",    when="+ramulator")
    depends_on("hbm-dramsim2",     when="+hbm")
    depends_on("nvdimmsim@2.0.0",  when="+hybridsim")
    depends_on("gettext")

    depends_on('autoconf@1.68:', type='build', when='@master:')
    depends_on('automake@1.11.1:', type='build', when='@master:')
    depends_on('libtool@1.2.4:', type='build', when='@master:')
    depends_on('m4', type='build', when='@master:')

    # force out-of-source builds
    build_directory = 'spack-build'

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('autogen.sh')

    def configure_args(self):
        args = []
        if '+pdes_mpi' in self.spec["sst-core"]:
            env['CC'] = self.spec['mpi'].mpicc
            env['CXX'] = self.spec['mpi'].mpicxx
            env['F77'] = self.spec['mpi'].mpif77
            env['FC'] = self.spec['mpi'].mpifc

        if "+pin" in self.spec:
            args.append("--with-pin=%s" % self.spec["intel-pin"].prefix)

        if "+dramsim2" in self.spec or "+hybridsim" in self.spec:
            args.append("--with-dramsim=%s" % self.spec["dramsim2"].prefix)

        if "+nvdimmsim" in self.spec or "+hybridsim" in self.spec:
            args.append("--with-nvdimmsim=%s" % self.spec["nvdimmsim"].prefix)

        if "+hybridsim" in self.spec:
            args.append("--with-hybridsim=%s" % self.spec["hybridsim"].prefix)

        if "+goblin" in self.spec:
            args.append("--with-goblin-hmcsim=%s" %
                        self.spec["goblin-hmc-sim"].prefix)

        if "+hbm" in self.spec:
            args.append("--with-hbmdramsim=%s" %
                        self.spec["hbm-dramsim2"].prefix)

        if "+ramulator" in self.spec:
            args.append("--with-ramulator=%s" % self.spec["ramulator"].prefix)

        args.append("--with-sst-core=%s" % self.spec["sst-core"].prefix)
        return args
