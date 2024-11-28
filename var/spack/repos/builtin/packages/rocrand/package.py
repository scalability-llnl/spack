# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Rocrand(CMakePackage):
    """The rocRAND project provides functions that generate
    pseudo-random and quasi-random numbers."""

    homepage = "https://github.com/ROCm/rocRAND"
    git = "https://github.com/ROCm/rocRAND.git"
    url = "https://github.com/ROCm/rocRAND/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["librocrand"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("6.2.1", sha256="ed07f638b5e30199251ddda6dd9ee53ee0ec49bcf37cc571a3de85c3a9833248")
    version("6.2.0", sha256="7f5318e9c9eb36fb3660392e97520268920c59af3a51af19633aabe5046ef1af")
    version("6.1.2", sha256="ac3c858c0f76188ac50574591aa6b41b27bda2af5925314451a44242319f28c8")
    version("6.1.1", sha256="d6302d014045694be85385cdc683ea75476e23fd92ae170079c261c0b041764b")
    version("6.1.0", sha256="ea80c5d657fa48b1122a47986239a04118977195ee4826d2b14b8bfe0fabce6e")
    version("6.0.2", sha256="51d66c645987cbfb593aaa6be94109e87fe4cb7e9c70309eb3c159af0de292d7")
    version("6.0.0", sha256="cee93231c088be524bb2cb0e6093ec47e62e61a55153486bebbc2ca5b3d49360")
    version("5.7.1", sha256="885cd905bbd23d02ba8f3f87d5c0b79bc44bd020ea9af190f3959cf5aa33d07d")
    version("5.7.0", sha256="d6053d986821e5cbc6cfec0778476efb1411ef943f11e7a8b973b1814a259dcf")
    version("5.6.1", sha256="6bf71e687ffa0fcc1b00e3567dd43da4147a82390f1b2db5e6f1f594dee6066d")
    version("5.6.0", sha256="cc894d2f1af55e16b62c179062063946609c656043556189c656a115fd7d6f5f")
    version("5.5.1", sha256="e8bed3741b19e296bd698fc55b43686206f42f4deea6ace71513e0c48258cc6e")
    version("5.5.0", sha256="0481e7ef74c181026487a532d1c17e62dd468e508106edde0279ca1adeee6f9a")
    with default_args(deprecated=True):
        version("5.4.3", sha256="463aa760e9f74e45b326765040bb8a8a4fa27aaeaa5e5df16f8289125f88a619")
        version("5.4.0", sha256="0f6a0279b8b5a6dfbe32b45e1598218fe804fee36170d5c1f7b161c600544ef2")
        version("5.3.3", sha256="b0aae79dce7f6f9ef76ad2594745fe1f589a7b675b22f35b4d2369e7d5e1985a")
        version("5.3.0", sha256="be4c9f9433415bdfea50d9f47b8afb43ac315f205ed39674f863955a6c256dca")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant("hiprand", default=True, when="@5.1.0:", description="Build the hiprand library")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("cmake@3.10.2:", type="build")

    depends_on("googletest@1.10.0:", type="test")

    # This patch ensures that libhiprand.so searches for librocrand.so in its
    # own directory first thanks to the $ORIGIN RPATH setting. Otherwise,
    # libhiprand.so cannot find dependency librocrand.so despite being in the
    # same directory.
    patch(
        "hiprand_prefer_samedir_rocrand.patch", working_dir="hiprand", when="@5.2.0:5.4 +hiprand"
    )

    # Add hiprand sources thru the below
    for d_version, d_commit in [
        ("5.4.3", "125d691d3bcc6de5f5d63cf5f5a993c636251208"),
        ("5.4.0", "125d691d3bcc6de5f5d63cf5f5a993c636251208"),
        ("5.3.3", "12e2f070337945318295c330bf69c6c060928b9e"),
        ("5.3.0", "12e2f070337945318295c330bf69c6c060928b9e"),
    ]:
        resource(
            name="hipRAND",
            git="https://github.com/ROCm/hipRAND.git",
            commit=d_commit,
            destination="",
            placement="hiprand",
            when=f"@{d_version} +hiprand",
        )
    resource(
        name="hipRAND",
        git="https://github.com/ROCm/hipRAND.git",
        branch="master",
        destination="",
        placement="hiprand",
        when="@master +hiprand",
    )
    resource(
        name="hipRAND",
        git="https://github.com/ROCm/hipRAND.git",
        branch="develop",
        destination="",
        placement="hiprand",
        when="@develop +hiprand",
    )

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
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")

    def patch(self):
        if self.spec.satisfies("@5.1.0:5.4 +hiprand"):
            os.rmdir("hipRAND")
            os.rename("hiprand", "hipRAND")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)
        if self.spec.satisfies("+asan"):
            env.set("CC", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
            env.set("CXX", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++")
            env.set("ASAN_OPTIONS", "detect_leaks=0")
            env.set("CFLAGS", "-fsanitize=address -shared-libasan")
            env.set("CXXFLAGS", "-fsanitize=address -shared-libasan")
            env.set("LDFLAGS", "-fuse-ld=lld")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        args = [self.define("BUILD_BENCHMARK", "OFF"), self.define("BUILD_TEST", self.run_tests)]

        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.1.0:5.4"):
            args.append(self.define_from_variant("BUILD_HIPRAND", "hiprand"))
        else:
            args.append(self.define("BUILD_HIPRAND", "OFF"))

        return args
