# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Migraphx(CMakePackage):
    """AMD's graph optimization engine."""

    homepage = "https://github.com/ROCm/AMDMIGraphX"
    git = "https://github.com/ROCm/AMDMIGraphX.git"
    url = "https://github.com/ROCm/AMDMIGraphX/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libmigraphx"]

    license("MIT")
    version("6.2.1", sha256="a9479fd6846bae4a888f712c2fecee6a252951ae8979d9990b100450e4cd6c30")
    version("6.2.0", sha256="7b36c1a0c44dd21f31ce6c9c4e7472923281aa7fdc693e75edd2670b101a6d48")
    version("6.1.2", sha256="829f4a2bd9fe3dee130dfcca103ddc7691da18382f5b683aaca8f3ceceaef355")
    version("6.1.1", sha256="e14a62678e97356236b45921e24f28ff430d670fb70456c3e5ebfeeb22160811")
    version("6.1.0", sha256="2ba44146397624845c64f3898bb1b08837ad7a49f133329e58eb04c05d1f36ac")
    version("6.0.2", sha256="13f393f8fdf25275994dda07091a93eec867233cd2f99f9cb0df16fbabd53483")
    version("6.0.0", sha256="7bb3f5011da9b1f3b79707b06118c523c1259215f650c2ffa5622a7e1d88868f")
    version("5.7.1", sha256="3e58c043a5a7d1357ee05725fd6cd41e190b070f1ba57f61300128429902089c")
    version("5.7.0", sha256="14f13554367d2d6490d66f8b5b739203225e7acce25085559e7c4acf29e2a4d5")
    version("5.6.1", sha256="b108c33f07572ffd880b20f6de06f1934ab2a1b41ae69095612322ac412fa91c")
    version("5.6.0", sha256="eaec90535d62002fd5bb264677ad4a7e30c55f18d2a287680d0495c7e60432b2")
    version("5.5.1", sha256="e71c4744f8ef6a1a99c179bbad94b8fe9bd7686eaa9397f376b70988c3341f0c")
    version("5.5.0", sha256="6084eb596b170f5e38f22b5fa37e66aa43a8cbc626712c9f03cde48c8fecfc8f")
    with default_args(deprecated=True):
        version("5.4.3", sha256="f83e7bbe5d6d0951fb2cf0abf7e8b3530e9a5e45f7cec6d760da055d6905d568")
        version("5.4.0", sha256="b6e7f4a1bf445ea0dae644ed5722369cde66fbee82a5917722f5d3f8c48b0a8c")
        version("5.3.3", sha256="91d91902bbedd5e1951a231e8e5c9a328360b128c731912ed17c8059df38e02a")
        version("5.3.0", sha256="d0b7283f42e03fb38b612868b8c94f46f27a6e0b019ae95fde5b9086582a1c69")

    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("0001-Adding-nlohmann-json-include-directory.patch", when="@:5.5")
    # Restrict Python 2.7 usage to fix the issue below
    # https://github.com/spack/spack/issues/24429
    patch("0003-restrict-python-2.7-usage.patch", when="@5.2.0:5.4")
    patch("0004-restrict-python2.7-usage-for-5.5.0.patch", when="@5.5.0")
    patch("0005-Adding-half-include-directory-path-migraphx.patch", when="@5.6.0:5.7")
    patch("0006-add-option-to-turn-off-ck.patch", when="@5.7")
    patch(
        "https://github.com/ROCm/AMDMIGraphX/commit/728bea3489c97c9e1ddda0a0ae527ffd2d70cb97.patch?full_index=1",
        sha256="3a8afd32208aa4f59fb31f898d243287771ebd409c7af7a4a785c586081e3711",
        when="@6.0",
    )

    patch(
        "https://github.com/ROCm/AMDMIGraphX/commit/624f8ef549522f64fdddad7f49a2afe1890b0b79.patch?full_index=1",
        sha256="410d0fd49f5f65089cd4f540c530c85896708b4fd94c67d15c2c279158aea85d",
        when="@6.0",
    )
    patch("0003-add-half-include-directory-migraphx-6.0.patch", when="@6.0:")

    depends_on("cmake@3.5:", type="build")
    depends_on("protobuf", type="link")
    depends_on("blaze", type="build")
    depends_on("nlohmann-json", type="link")
    depends_on("msgpack-c", type="link")
    depends_on("half@1.12.0", type="link", when="@:5.5")
    depends_on("half@2:", when="@5.6:")
    depends_on("python@3.5:", type="build")
    depends_on("py-pybind11@2.6:", type="build", when="@4.1.0:")
    depends_on("pkgconfig", type="build", when="@5.3.0:")
    depends_on("abseil-cpp")

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
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        depends_on(f"rocblas@{ver}", when=f"@{ver}")
        depends_on(f"miopen-hip@{ver}", when=f"@{ver}")

    for ver in ["6.0.0", "6.0.2", "6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1"]:
        depends_on(f"rocmlir@{ver}", when=f"@{ver}")

    @property
    def cmake_python_hints(self):
        """Include the python include path to the
        CMake based on current spec
        """
        python = self.spec["python"]
        return [self.define("Python_INCLUDE_DIR", python.package.config_vars["include"])]

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def setup_build_environment(self, env):
        if self.spec.satisfies("+asan"):
            env.set("CC", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
            env.set("CXX", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++")
            env.set("ASAN_OPTIONS", "detect_leaks=0")
            env.set("CFLAGS", "-fsanitize=address -shared-libasan")
            env.set("CXXFLAGS", "-fsanitize=address -shared-libasan")
            env.set("LDFLAGS", "-fuse-ld=lld")

    def cmake_args(self):
        spec = self.spec
        abspath = spec["abseil-cpp"].prefix.include
        args = [
            self.define("CMAKE_CXX_COMPILER", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++"),
            self.define("NLOHMANN_JSON_INCLUDE", self.spec["nlohmann-json"].prefix.include),
        ]
        if self.spec["cmake"].satisfies("@3.16.0:"):
            args += self.cmake_python_hints
        if "@5.5.0:" in self.spec:
            args.append(self.define("CMAKE_CXX_FLAGS", "-I{0}".format(abspath)))
            args.append(self.define("MIGRAPHX_ENABLE_PYTHON", "OFF"))
        if "@5.7:" in self.spec:
            args.append(self.define("MIGRAPHX_USE_COMPOSABLEKERNEL", "OFF"))
            args.append(
                self.define("GPU_TARGETS", "gfx906;gfx908;gfx90a;gfx1030;gfx1100;gfx1101;gfx1102")
            )
        if self.spec.satisfies("@6.1:") and self.spec.satisfies("+asan"):
            args.append(
                self.define(
                    "CMAKE_CXX_FLAGS", "-fsanitize=address -shared-libasan -I{0}".format(abspath)
                )
            )
        return args

    def test_unit_tests(self):
        """Run installed UnitTests"""
        if self.spec.satisfies("@:5.5.0"):
            raise SkipTest("Package must be installed as version @5.5.1 or later")
        unit_tests = which(self.prefix.bin.UnitTests)
        assert unit_tests is not None, "UnitTests is not installed!"
        unit_tests()
