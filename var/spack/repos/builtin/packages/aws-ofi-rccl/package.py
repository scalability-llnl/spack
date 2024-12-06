# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AwsOfiRccl(AutotoolsPackage):
    """AWS OFI RCCL is a plug-in which enables EC2 developers to use
    libfabric as a network provider while running AMD's RCCL based
    applications."""

    homepage = "https://github.com/ROCm/aws-ofi-rccl"
    git = "https://github.com/ROCm/aws-ofi-rccl.git"
    url = "https://github.com/ROCm/aws-ofi-rccl.git"
    tags = ["rocm"]

    maintainers("bvanessen")

    license("Apache-2.0")

    version("cxi", branch="cxi", preferred=True)
    version("master", branch="master")

    depends_on("c", type="build")  # generated

    variant("trace", default=False, description="Enable printing trace messages")
    variant("tests", default=False, description="Build tests")

    depends_on("libfabric")
    depends_on("hip")
    depends_on("rccl")
    depends_on("mpi")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    # To enable this plug-in to work with RCCL add it to the LD_LIBRARY_PATH
    def setup_run_environment(self, env):
        aws_ofi_rccl_home = self.spec["aws-ofi-rccl"].prefix
        env.prepend_path("LD_LIBRARY_PATH", aws_ofi_rccl_home.lib)

    # To enable this plug-in to work with RCCL add it to the LD_LIBRARY_PATH
    def setup_dependent_run_environment(self, env, dependent_spec):
        aws_ofi_rccl_home = self.spec["aws-ofi-rccl"].prefix
        env.prepend_path("LD_LIBRARY_PATH", aws_ofi_rccl_home.lib)

    def configure_args(self):
        spec = self.spec
        args = []

        # Always set configure's external paths to use the Spack
        # provided dependencies
        args.extend(
            [
                "--with-libfabric={0}".format(spec["libfabric"].prefix),
                "--with-hip={0}".format(spec["hip"].prefix),
                "--with-rccl={0}".format(spec["rccl"].prefix),
                "--with-mpi={0}".format(spec["mpi"].prefix),
            ]
        )

        args.extend(self.enable_or_disable("trace"))
        args.extend(self.enable_or_disable("tests"))

        return args
