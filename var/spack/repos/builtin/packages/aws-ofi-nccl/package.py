# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AwsOfiNccl(AutotoolsPackage):
    """AWS OFI NCCL is a plug-in which enables EC2 developers to use
    libfabric as a network provider while running NVIDIA's NCCL based
    applications."""

    homepage = "https://github.com/aws/aws-ofi-nccl"
    url = "https://github.com/aws/aws-ofi-nccl/archive/v0.0.0.tar.gz"
    git = "https://github.com/aws/aws-ofi-nccl.git"

    maintainers("bvanessen")

    version("master", branch="master")
    version("1.8.1", sha256="beb59959be0f60b891f9549f4df51b394e97e739416c88c3436e75516fe067c8")
    version("1.8.0", sha256="a2f1750d4908924985335e513186353d0c4d9a5d27b1a759f6aa31a10e74c06d")
    version("1.7.4", sha256="472bbc977ce37d0cf9239b8e366f4f247226a984eb8c487aadd884af53f00e13")
    version("1.7.3", sha256="7a49b530eb0fa5e262c1fcf3412289bc1d538c15290435c579d5e7f08d806fd4")
    version("1.7.2", sha256="c89bbe5fa49a7036eb873c01c8fdc5693238ae010ddcaf10b10fdc88aec6e56a")
    version("1.7.1", sha256="d50a160c7aba76445e5c895fba0f3dbfdec51f702d218168a5e5017806cf0fb0")
    version("1.6.0", sha256="19a6fc91afe9a317fd3154c897fa219eab48fcdddefa66d881f1843c1165f7ee")

    depends_on("c", type="build")  # generated

    variant("trace", default=False, description="Enable printing trace messages")
    variant("tests", default=False, description="Build tests")

    depends_on("libfabric")
    depends_on("cuda")
    depends_on("nccl")
    depends_on("mpi")
    depends_on("hwloc", when="@1.7:")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def url_for_version(self, version):
        if version < Version("1.7.0"):
            return super().url_for_version(version)
        url_fmt = "https://github.com/aws/aws-ofi-nccl/archive/v{0}-aws.tar.gz"
        return url_fmt.format(version)

    # To enable this plug-in to work with NCCL add it to the LD_LIBRARY_PATH
    def setup_run_environment(self, env):
        aws_ofi_nccl_home = self.spec.prefix
        env.append_path("LD_LIBRARY_PATH", aws_ofi_nccl_home.lib)

    # To enable this plug-in to work with NCCL add it to the LD_LIBRARY_PATH
    def setup_dependent_run_environment(self, env, dependent_spec):
        aws_ofi_nccl_home = self.spec["aws-ofi-nccl"].prefix
        env.append_path("LD_LIBRARY_PATH", aws_ofi_nccl_home.lib)

    def configure_args(self):
        spec = self.spec
        args = []

        # Always set configure's external paths to use the Spack
        # provided dependencies
        args.extend(
            [
                "--with-libfabric={0}".format(spec["libfabric"].prefix),
                "--with-cuda={0}".format(spec["cuda"].prefix),
                "--with-nccl={0}".format(spec["nccl"].prefix),
                "--with-mpi={0}".format(spec["mpi"].prefix),
            ]
        )
        if spec.satisfies("@1.7:"):
            args.extend(["--with-hwloc={0}".format(spec["hwloc"].prefix)])

        args.extend(self.enable_or_disable("trace"))
        args.extend(self.enable_or_disable("tests"))

        return args
