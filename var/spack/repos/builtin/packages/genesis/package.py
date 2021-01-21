# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Genesis(AutotoolsPackage, CudaPackage):
    """GENESIS is a Molecular dynamics and modeling software
    for bimolecular systems such as proteins, lipids, glycans,
    and their complexes.
    """

    homepage = "https://www.r-ccs.riken.jp/labs/cbrt/"
    url = "https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2020/09/genesis-1.5.1.tar.bz2"
    git = "https://github.com/genesis-release-r-ccs/genesis-2.0.git"

    version('2.0b', branch='master')
    version('1.5.1', '28d696e681efd76cc8a875dc0b305794',
            url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2020/09/genesis-1.5.1.tar.bz2')

    resource(when='@1.5.1',
             name='user_guide',
             url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2019/10/GENESIS-1.4.0.pdf',
             sha256='da2c3f8bfa1e93adb992d3cfce09fb45d8d447a94f9a4f884ac834ea7279b9c7',
             expand=False,
             placement='doc')

    variant("openmp", default=True, description="Enable OpenMP.")
    variant("single", default=False, description="Enable single precision.")
    variant("hmdisk", default=False, description="Enable huge molecule on hard disk.")
    variant("fugaku", default=False, description="Enable Fugaku option")

    conflicts("%clang", when="+openmp")
    conflicts('+fugaku', when="@:1.9.9", msg='Fugaku option is not available.')

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("mpi", type=("build", "run"))
    depends_on("lapack")

    patch("fj_compiler.patch", when="%fj")

    parallel = False

    def configure_args(self):
        spec = self.spec
        options = []
        options.extend(self.enable_or_disable("openmp"))
        options.extend(self.enable_or_disable("single"))
        options.extend(self.enable_or_disable("hmdisk"))
        if "+cuda" in spec:
            options.append('--enable-gpu')
            options.append("--with-cuda=%s" % spec["cuda"].prefix)
        else:
            options.append('--disable-gpu')
        if "+fugaku" in spec:
            options.append("--host=Fugaku")
        return options

    def setup_build_environment(self, env):
        env.set("FC", self.spec["mpi"].mpifc, force=True)
        env.set("F77", self.spec["mpi"].mpif77, force=True)
        env.set("CC", self.spec["mpi"].mpicc, force=True)
        env.set("CXX", self.spec["mpi"].mpicxx, force=True)
        env.set("LAPACK_LIBS", "{0}".format(self.spec["lapack"].libs.ld_flags))
        if "+cuda" in self.spec:
            cuda_arch = self.spec.variants['cuda_arch'].value
            cuda_gencode = ' '.join(self.cuda_flags(cuda_arch))
            env.set("NVCCFLAGS", cuda_gencode)

    def install(self, spec, prefix):
        make("install")
        install_tree('doc', prefix.share.doc)
