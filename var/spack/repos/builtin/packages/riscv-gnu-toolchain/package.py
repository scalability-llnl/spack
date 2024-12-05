# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shlex
from subprocess import Popen

from spack.package import *


class RiscvGnuToolchain(AutotoolsPackage):
    """A cross-compilation tool for RISC-V."""

    homepage = "https://spack-tutorial.readthedocs.io/"
    git = "https://github.com/riscv-collab/riscv-gnu-toolchain.git"

    maintainers("wanlinwang")

    version("develop", branch="master", submodules=True)
    version(
        "2024.02.02",
        tag="2024.02.02",
        commit="59ab58e8a4aed4ed8f711ebab307757a5ebaa1f5",
        submodules=True,
    )
    version(
        "2023.12.20",
        tag="2023.12.20",
        commit="8c969a9efe68a811cf524174d25255632029f3d3",
        submodules=True,
    )
    version(
        "2023.12.14",
        tag="2023.12.14",
        commit="99e2d2bac5144f5152ba6d3fbf04bdd9b9ba4381",
        submodules=True,
    )
    version(
        "2023.12.12",
        tag="2023.12.12",
        commit="ae9efcc33c4968f97ab89b4b13c7f6520b145f94",
        submodules=True,
    )
    version(
        "2023.11.22",
        tag="2023.11.22",
        commit="8e9fb09a0c4b1e566492ee6f42e8c1fa5ef7e0c2",
        submodules=True,
    )
    version(
        "2023.11.20",
        tag="2023.11.20",
        commit="82c3d6550a26f03c3b4acb6cbefe5c5e98855ddb",
        submodules=True,
    )
    version(
        "2023.11.17",
        tag="2023.11.17",
        commit="9b2ad263050085543a1ad57c13039e49a79a7def",
        submodules=True,
    )
    version(
        "2023.11.08",
        tag="2023.11.08",
        commit="b86b2b37d0acc607156ff56ff17ee105a9b48897",
        submodules=True,
    )
    version(
        "2023.10.18",
        tag="2023.10.18",
        commit="b86b2b37d0acc607156ff56ff17ee105a9b48897",
        submodules=True,
    )
    version(
        "2023.10.17",
        tag="2023.10.17",
        commit="c11f0748276c58df4f9d9602cdc2de5f17cbae8c",
        submodules=True,
    )
    version(
        "2023.10.12",
        tag="2023.10.12",
        commit="e65e7fc58543c821baf4f1fb6d0ef700177b9d89",
        submodules=True,
    )
    version(
        "2023.10.06",
        tag="2023.10.06",
        commit="6e7190e8c95e09d541e69f6f6e39163f808570d5",
        submodules=True,
    )
    version(
        "2023.09.27",
        tag="2023.09.27",
        commit="5afde2de23c6597aaa5069f36574c61bcb39b007",
        submodules=True,
    )
    version(
        "2023.09.26",
        tag="2023.09.26",
        commit="ffb5968884630c7baebba7b2af493f6b5f74ad80",
        submodules=True,
    )
    version(
        "2023.09.13",
        tag="2023.09.13",
        commit="5437780994b830e9eabf467f85f22ed24b5fade1",
        submodules=True,
    )
    version(
        "2022.08.08",
        tag="2022.08.08",
        commit="cb25bb862a3bf56d1577d7930bc41f259632ae24",
        submodules=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Dependencies:
    depends_on("pkgconfig", type="build")
    depends_on("autoconf", when="@main:", type="build")
    depends_on("python", type="build")
    depends_on("gawk", type="build")
    depends_on("bison", type="build")
    depends_on("flex@:2.6.1,2.6.4:", type="build")
    depends_on("texinfo", type="build")
    depends_on("patchutils", type="build")
    depends_on("mpc", type="build")
    depends_on("gmp", type="build")
    depends_on("mpfr", type="build")
    depends_on("zlib-api", type=("build", "link"))
    depends_on("expat", type=("build", "link"))
    depends_on("bzip2", type="build")
    depends_on("gmake@4.3:", type="build")

    conflicts("platform=windows", msg="Windows is not supported.")
    conflicts("arch=aarch64", msg="aarch64 is not supported.")

    variant(
        "compiler_type",
        default="newlib",
        values=("newlib", "linux", "musl"),
        description="Compiler back-end to build",
    )

    variant("multilib", default=False, description="Enable multilib support")
    variant(
        "cmodel",
        default="medlow",
        values=("medlow", "medany"),
        description="The name of the cmodel",
    )

    def configure_args(self):
        args = super(RiscvGnuToolchain, self).configure_args()
        if "+multilib" in self.spec:
            args.append("--enable-multilib")

        cmodel_value = self.spec.variants["cmodel"].value
        if cmodel_value:
            args.append("--with-cmodel={}".format(cmodel_value))
        return args

    def build(self, spec, prefix):
        """Makes the build targets specified by
        :py:attr:``~.AutotoolsPackage.build_targets``
        """
        with working_dir(self.stage.source_path):
            # modify Makefile not to git init submodules.
            cmd = "/bin/sed -i.bak -r \
            '/^# Rule for auto init submodules/,/git submodule update.*$/d' \
            Makefile"
            p = Popen(shlex.split(cmd))
            p.wait()
            p.communicate()

            params = []
            if self.spec.satisfies("compiler_type=linux"):
                params.append("linux")
            elif self.spec.satisfies("compiler_type=musl"):
                params.append("musl")

            make(*params)
