# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RocprofilerDev(CMakePackage):
    """ROCPROFILER library for AMD HSA runtime API extension support"""

    homepage = "https://github.com/ROCm/rocprofiler"
    git = "https://github.com/ROCm/rocprofiler.git"
    url = "https://github.com/ROCm/rocprofiler/archive/refs/tags/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocprofiler64"]
    license("MIT")
    version("6.2.1", sha256="6eb36dad67e3b294f210e21987c52aec666652cffa87b8af1f8077d5b7812245")
    version("6.2.0", sha256="79b4f29d051e62639b4bf2ca288035514d32e055fc759ff4a82d377bf7ca97ea")
    version("6.1.2", sha256="e6e8771b8c933c16a99192cc215fe964a95e1718ad286520c8272150e184bc06")
    version("6.1.1", sha256="b4b01a02de5328c7383c2318a998da86a6a9372e1728fc88a21b52bc1cbe9d9d")
    version("6.1.0", sha256="14ac0a451428465133583e83d9177ed34b3d4679515018a12ee74f5e0288c956")
    version("6.0.2", sha256="d3f24e639a5e151fa418a92ae6fe150bdf14120b8982a5baa52844ce2fba0b82")
    version("6.0.0", sha256="6aca327a6ba302b5957002e55ac640dd185d51a354da3859e957448a5fc36b14")
    version("5.7.1", sha256="2fb7158592d89312ba419a272d907d8849373c0a676a83dd03c32b9942dfd27a")
    version("5.7.0", sha256="003af33db5585e71823b2b58618d795df926f6bd25943f2add388db23f2bf377")
    version("5.6.1", sha256="3e5eecce216418e61ffee893cbc8611e38305ee472d0e10d579eb74e287c8e1b")
    version("5.6.0", sha256="ff811bd91580f60b6b4d397b6fce38d96f07debc6fd8a631b81d1b266cc9542d")
    version("5.5.1", sha256="f5dbece5c205e37383fed4a2bd6042ff1c11f11f64dfbf65d7e23c0af6889a5a")
    version("5.5.0", sha256="d9dd38c42b4b12d4149f1cc3fca1af5bec69c72f455653a8f4fd8195b3b95703")
    with default_args(deprecated=True):
        version("5.4.3", sha256="86c3f43ee6cb9808796a21409c853cc8fd496578b9eef4de67ca77830229cac1")
        version("5.4.0", sha256="0322cbe5d1d3182e616f472da31f0707ad6040833c38c28f2b39381a85210f43")
        version("5.3.3", sha256="07ee28f3420a07fc9d45910e78ad7961b388109cfc0e74cfdf2666789e6af171")
        version("5.3.0", sha256="b0905a329dc1c97a362b951f3f8ef5da9d171cabb001ed4253bd59a2742e7d39")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3:", type="build")

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
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", when=f"@{ver}")
        depends_on(f"roctracer-dev-api@{ver}", when=f"@{ver}")

    for ver in ["5.7.0", "5.7.1", "6.0.0", "6.0.2", "6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-smi-lib@{ver}", when=f"@{ver}")

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
        depends_on(f"aqlprofile@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")

    depends_on("numactl", type="link", when="@4.3.1")
    depends_on("py-lxml", when="@5.5:")
    depends_on("py-cppheaderparser", when="@5.5:")
    depends_on("googletest@1.10.0:", when="@5.5:")
    depends_on("py-pyyaml", when="@5.5:")
    depends_on("py-barectf", when="@5.5:")
    depends_on("py-setuptools", when="@5.5:")
    depends_on("py-jsonschema", when="@5.5:")
    depends_on("py-jinja2", when="@5.5:")
    depends_on("py-termcolor", when="@5.5:")
    depends_on("py-pandas", when="@6.0:")

    # See https://github.com/ROCm/rocprofiler/pull/50
    patch("fix-includes.patch", when="@:5.4")
    patch("0001-Continue-build-in-absence-of-aql-profile-lib.patch", when="@5.3:5.4")
    patch("0002-add-fPIC-and-disable-tests.patch", when="@5.5")
    patch("0002-add-fPIC-and-disable-tests-5.6.patch", when="@5.6")
    patch("0002-add-fPIC-and-disable-tests-5.7.patch", when="@5.7")
    patch("0003-disable-tests.patch", when="@6.0:")

    def patch(self):
        filter_file(
            "${HSA_RUNTIME_LIB_PATH}/../include",
            "${HSA_RUNTIME_LIB_PATH}/../include ${HSA_KMT_LIB_PATH}/..\
                     /include",
            "test/CMakeLists.txt",
            string=True,
        )

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        args = [
            self.define(
                "PROF_API_HEADER_PATH", self.spec["roctracer-dev-api"].prefix.roctracer.include.ext
            ),
            self.define("ROCM_ROOT_DIR", self.spec["hsakmt-roct"].prefix.include),
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
        ]
        if self.spec.satisfies("@6.2:"):
            args.append(self.define("ROCPROFILER_BUILD_PLUGIN_PERFETTO", "OFF"))
        return args

    @run_after("install")
    def post_install(self):
        if self.spec.satisfies("@6.0:"):
            install_tree(self.prefix.include.rocprofiler, self.prefix.rocprofiler.include)
            install_tree(self.prefix.lib, self.prefix.rocprofiler.lib)
