# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RocmDbgapi(CMakePackage):
    """The AMD Debugger API is a library that provides all the support
    necessary for a debugger and other tools to perform low level
    control of the execution and inspection of execution state of
    AMD's commercially available GPU architectures."""

    homepage = "https://github.com/ROCm/ROCdbgapi"
    git = "https://github.com/ROCm/ROCdbgapi.git"
    url = "https://github.com/ROCm/ROCdbgapi/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm-dbgapi"]

    license("MIT")

    version("master", branch="amd-master")
    version("6.2.1", sha256="40064ca031e41ff3c87bfa31406b7192fa65709ab36734eddad87e0ecc01bb80")
    version("6.2.0", sha256="311811ce0970ee83206791c21d539f351ddeac56ce3ff7efbefc830038748c0c")
    version("6.1.2", sha256="6e55839e3d95c2cfe3ff89e3e31da77aeecc74012a17f5308589e8808df78026")
    version("6.1.1", sha256="425a6cf6a3942c2854c1f5e7717bed906cf6c3753b46c44476f54bfef6188dac")
    version("6.1.0", sha256="0985405b6fd44667a7ce8914aa39a7e651613e037e649fbdbfa2adcf744a2d50")
    version("6.0.2", sha256="39036f083de421f46afd8d3a8799576242ef64002643d7185767ccbba41ae854")
    version("6.0.0", sha256="4e823eba255e46b93aff05fd5938ef2a51693ffd74debebffc1aabfce613805c")
    version("5.7.1", sha256="0ee9c2f083868849f2ea0cec7010e0270c27e7679ccbbadd12072cc0ef6c8a6f")
    version("5.7.0", sha256="285ddded8e7f1981d8861ffc1cd7770b78129e4955da08ad55a4779945699716")
    version("5.6.1", sha256="c7241bf94bdb97a4cf1befbf25b8c35720797710da6f6b5b9d6a4094c1bc9c8b")
    version("5.6.0", sha256="9b66e47f4eccb3c8bbc324aade92aac6139539dda449427b7823d0c45341afc8")
    version("5.5.1", sha256="c41dfc62591bcf42003fe744d8bd03a51311d54e4b012f946ca0ede0c14dd977")
    version("5.5.0", sha256="ce572340a3fe99e4f1538eb614933153456003f8dfe9306a5735cdd25b451e25")
    with default_args(deprecated=True):
        version("5.4.3", sha256="d647c9121a50f2c54367c567d8f39a145cb135e1ceed931581659f57f49f61e5")
        version("5.4.0", sha256="895eb7056864daada40c3f9cd37645b0bdf4b6dc408b5f8cc974fc4cd9ab7ccb")
        version("5.3.3", sha256="3c81cb23fe671d391557a63c13b6a13d4dc367db5cb5de55592a6758284d8a3f")
        version("5.3.0", sha256="afffec78e34fe70952cd41efc3d7ba8f64e43acb2ad20aa35c9b8b591bed48ca")

    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("cxx", type="build")  # generated
    depends_on("cmake@3:", type="build")
    depends_on("hwdata", when="@5.5.0:")

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
        "master",
    ]:
        depends_on(f"hsa-rocr-dev@{ver}", type="build", when=f"@{ver}")
        depends_on(f"comgr@{ver}", type=("build", "link"), when=f"@{ver}")

    for ver in [
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
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def patch(self):
        filter_file(
            r"(<INSTALL_INTERFACE:include>)",
            r"\1 {0}/include".format(self.spec["hsa-rocr-dev"].prefix),
            "CMakeLists.txt",
        )

    def setup_build_environment(self, env):
        if self.spec.satisfies("+asan"):
            env.set("CC", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
            env.set("CXX", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++")
            env.set("ASAN_OPTIONS", "detect_leaks=0")
            env.set("CFLAGS", "-fsanitize=address -shared-libasan")
            env.set("CXXFLAGS", "-fsanitize=address -shared-libasan")
            env.set("LDFLAGS", "-fuse-ld=lld")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))
        return args
