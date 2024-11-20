# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hipfort(CMakePackage):
    """Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCm/hipfort"
    git = "https://github.com/ROCm/hipfort.git"
    url = "https://github.com/ROCm/hipfort/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    license("MIT")

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    version("6.2.1", sha256="5258f2dd63aeebe29ce566e654c47b8e2e1f5eb8ca3da92af09c54517b259f32")
    version("6.2.0", sha256="7f6db61a0ac7771e5c4604a6113b36736f6c7f05cabd7e1df8e832c98b87311d")
    version("6.1.2", sha256="f60d07fa3e5b09246c8908b2876addf175a91e91c8b0fac85b000f88b6743c7c")
    version("6.1.1", sha256="646f7077399db7a70d7102fda8307d0a11039f616399a4a06a64fd824336419f")
    version("6.1.0", sha256="70d3ccc9f3536f62686e73934f5972ed011c4df7654ed1f8e6d2d42c4289f47e")
    version("6.0.2", sha256="b60ada7474b71c1d82c700b0159bc0756dbb2808375054903710280b1677f199")
    version("6.0.0", sha256="151cf11648885db799aade0d00a7882589e7195643b02beaa251f1b2a43aceed")
    version("5.7.1", sha256="859fac509e195f3ab97c555b5f63afea325a61aae0f281cb19a970a1b533dead")
    version("5.7.0", sha256="57b04d59f61683a1b141d6d831d10c9fdecea483991ec02d14c14e441e935c05")
    version("5.6.1", sha256="a55345cc9ccaf0cd69d306b8eb9ec2a02c220a57e9c396443cc7273aa3377adc")
    version("5.6.0", sha256="03176a099bc81e212ad1bf9d86f35561f8f2d21a2f126732d7620e1ea59888d5")
    version("5.5.1", sha256="abc59f7b81cbefbe3555cbf1bf0d80e8aa65901c70799748c40870fe6f3fea60")
    version("5.5.0", sha256="cae75ffeac129639cabebfe2f95f254c83d6c0a6cffd98142ea3537a132e42bb")
    with default_args(deprecated=True):
        version("5.4.3", sha256="1954a1cba351d566872ced5549b2ced7ab6332221e2b98dba3c07180dce8f173")
        version("5.4.0", sha256="a781bc6d1dbb508a4bd6cc3df931696fac6c6361d4fd35efb12c9a04a72e112c")
        version("5.3.3", sha256="593be86502578b68215ffe767c26849fd27d4dbd92c8e76762275805f99e64f5")
        version("5.3.0", sha256="9e2aa142de45b2d2c29449d6f82293fb62844d511fbf51fa597845ba05c700fa")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.0.2:", type="build")

    depends_on("rocm-cmake@3.8.0:", type="build")

    depends_on("binutils", when="%cce")

    for ver in [
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on(f"hip@{ver}", type="build", when=f"@{ver}")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = []

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("%cce"):
            args.append("-DHIPFORT_COMPILER={}".format(spack_fc))
            args.append("-DHIPFORT_AR=" + join_path(self.spec["binutils"].prefix.bin, "ar"))
            args.append(
                "-DHIPFORT_RANLIB=" + join_path(self.spec["binutils"].prefix.bin, "ranlib")
            )
            args.append("-DHIPFORT_COMPILER_FLAGS='-ffree -eT'")
        elif self.spec.satisfies("%gcc"):
            args.append("-DHIPFORT_COMPILER={}".format(spack_fc))
            args.append("-DHIPFORT_COMPILER_FLAGS='-ffree-form -cpp -ffree-line-length-none'")

        return args
