# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpifileutils(CMakePackage):
    """mpiFileUtils is a suite of MPI-based tools to manage large datasets,
    which may vary from large directory trees to large files.
    High-performance computing users often generate large datasets with
    parallel applications that run with many processes (millions in some
    cases). However those users are then stuck with single-process tools
    like cp and rm to manage their datasets. This suite provides
    MPI-based tools to handle typical jobs like copy, remove, and compare
    for such datasets, providing speedups of up to 20-30x."""

    homepage = "https://github.com/hpc/mpifileutils"
    url = "https://github.com/hpc/mpifileutils/archive/v0.9.tar.gz"
    git = "https://github.com/hpc/mpifileutils.git"

    tags = ["e4s"]

    license("BSD-3-Clause")

    version("develop", branch="main")
    version("0.11.1", sha256="e2cba53309b5b3ee581b6ff82e4e66f54628370cce694c34224ed947fece32d4")
    version("0.11", sha256="f5dc1b39077b3c04f79b2c335c4fd80306f8c57ecfbcacbb82cf532caf02b5fd")
    version("0.10.1", sha256="4c8409ef4140f6f557d0e93f0c1267baf5d893c203b29fb7a33d9bc3c5a5d25c")
    version("0.10", sha256="5a71a9acd9841c3c258fc0eaea942f18abcb40098714cc90462b57696c07e3c5")
    version("0.9.1", sha256="15a22450f86b15e7dc4730950b880fda3ef6f59ac82af0b268674d272aa61c69")
    version("0.9", sha256="1b8250af01aae91c985ca5d61521bfaa4564e46efa15cee65cd0f82cf5a2bcfb")

    depends_on("c", type="build")  # generated

    variant("xattr", default=True, description="Enable code for extended attributes")
    variant("lustre", default=False, description="Enable optimizations and features for Lustre")
    variant("gpfs", default=False, description="Enable optimizations and features for GPFS")
    variant("experimental", default=False, description="Install experimental tools")
    variant("daos", default=False, description="Enable DAOS support", when="@0.11:")

    patch("nosys_getdents.patch", when="@:0.10.1 target=aarch64:")

    conflicts("platform=darwin")

    depends_on("mpi")
    depends_on("libcircle")

    # DTCMP_Segmented_exscan renamed in v1.1.0
    depends_on("dtcmp@1.1.0:")

    # fixes were added to libarchive somewhere between 3.1.2 and 3.5.0
    # which helps with file names that start with "._", bumping to newer
    # libarchive, but in a way that does not disrupt older mpiFileUtils installs
    depends_on("libarchive")
    depends_on("libarchive@3.5.1:", when="@0.11:")

    depends_on("attr", when="@0.11.1:+xattr")
    depends_on("daos", when="+daos")
    depends_on("bzip2")
    depends_on("libcap")
    depends_on("openssl")
    depends_on("cmake@3.1:", type="build")

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "cflags":
            if spec.satisfies("%oneapi"):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    def cmake_args(self):
        args = [
            self.define("WITH_DTCMP_PREFIX", self.spec["dtcmp"].prefix),
            self.define("WITH_LibCircle_PREFIX", self.spec["libcircle"].prefix),
            self.define_from_variant("ENABLE_XATTRS", "xattr"),
            self.define_from_variant("ENABLE_LUSTRE", "lustre"),
            self.define_from_variant("ENABLE_GPFS", "gpfs"),
            self.define_from_variant("ENABLE_EXPERIMENTAL", "experimental"),
        ]

        if self.spec.satisfies("+daos"):
            args.append(self.define("ENABLE_DAOS", True))
            args.append(self.define("WITH_DAOS_PREFIX", self.spec["daos"].prefix))
        else:
            args.append(self.define("ENABLE_DAOS", False))

        return args
