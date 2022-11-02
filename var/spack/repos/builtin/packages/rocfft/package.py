# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rocfft(CMakePackage):
    """Radeon Open Compute FFT library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocFFT/"
    git = "https://github.com/ROCmSoftwarePlatform/rocFFT.git"
    url = "https://github.com/ROCmSoftwarePlatform/rocfft/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["librocfft"]

    version("5.4.3", sha256="ed9664adc9825c237327497bc4b23f020d50be7645647f14a45f4d943dd506e7")
    version("5.4.0", sha256="d35a67332f4425fba1824eed78cf98d5c9a17a422614ff3f4cba2461df952336")
    version("5.3.3", sha256="678c18710578c1fb36a0009311bb79de7607c3468f9102cfba56a866ebb7ff78")
    version("5.3.0", sha256="d655c5541c4aff4267e80e36d002fc3a55c2f84a0ae8631197c12af3bf03fa7d")
    version("5.2.3", sha256="0cee37886f01f1afb3ae5dad1164c819573c13c6675bff4eb668de334adbff27")
    version("5.2.1", sha256="6302349b6cc610a9a939377e2c7ffba946656a8d43f2e438ff0b3088f0f963ad")
    version("5.2.0", sha256="ebba280b7879fb4bc529a68072b98d4e815201f90d24144d672094bc241743d4")
    version("5.1.3", sha256="b4fcd03c1b07d465bb307ec33cc7fb50036dff688e497c5e52b2dec37f4cb618")
    version("5.1.0", sha256="dc11c9061753ae43a9d5db9c4674aa113a8adaf50818b2701cbb940894147f68")
    version(
        "5.0.2",
        sha256="30d4bd5fa85185ddafc69fa6d284edd8033c9d77d1e351fa328267242995eb0a",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="c16374dac2f85fbaf145511653e93f6db3151425ce39b282187745c716b67405",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="2724118ca00b9e97ac9578fe0b7e64a82d86c4fb0246d0da88d8ddd9c608b1e1",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="045c1cf1737db6e7ee332c274dacdb565f99c976ed4cc5626a116878dc80a48c",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="fcdc4d12b93d967b6f992b4045da98433eabf2ee0ba84fc6b6f81e380584fbc9",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="cb5b8f62330bc61b17a3a2fd1500068ee05d48cb51797901dd259dbc84610478",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="db29c9067f0cfa98bddd3574f6aa7200cfc790cc6da352d19e4696c3f3982163",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="df23fcb05aae72557461ae3687be7e3b8b78be4132daf1aa9dc07339f4eba0cc",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="d1d10d270f822e0bab64307313ef163ba449b058bf3352962bbb26d4f4db89d0",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="9f57226aac7d9a0515e14a5a5b08a85e727de72b3f9c2177daf56749ac2c76ae",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="9c9c0b7f09bab17250f5101d1605e7a61218eae828a3eb8fe048d607181294ce",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="ed23009796e2ee7c43dcc24527f2d6b1d7a73dceac06c30384460098d2fe1556",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="94462e4bd19c2c749fcf6903adbee66d4d3bd345c0246861ff8f40b9d08a6ead",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="629f02cfecb7de5ad2517b6a8aac6ed4de60d3a9c620413c4d9db46081ac2c88",
        deprecated=True,
    )

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.16:", type="build", when="@4.5.0:")
    depends_on("cmake@3.5:", type="build")
    depends_on("python@3.6:", type="build", when="@5.0.0:")
    depends_on("sqlite@3.36:", when="@5.0.0:")

    depends_on("googletest@1.10.0:", type="test")
    depends_on("fftw@3.3.8:", type="test")
    depends_on("boost@1.64.0: +program_options", type="test")
    depends_on("llvm-amdgpu +openmp", type="test")

    def check(self):
        exe = join_path(self.build_directory, "clients", "staging", "rocfft-test")
        self.run_test(exe, options="--gtest_filter=mix*:adhoc*")

    for ver in [
        "3.5.0",
        "3.7.0",
        "3.8.0",
        "3.9.0",
        "3.10.0",
        "4.0.0",
        "4.1.0",
        "4.2.0",
        "4.3.0",
        "4.3.1",
        "4.5.0",
        "4.5.2",
        "5.0.0",
        "5.0.2",
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
    ]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("rocm-config" + ver, when="@" + ver)

    patch("0001-Improve-compilation-by-using-sqlite-recipe-for-rocfft.patch", when="@5.0.0:5.0.2")
    # Patch to add spack build test support. No longer required from 5.2
    patch("0002-Fix-clients-fftw3-include-dirs-rocm-4.2.patch", when="@4.2.0:4.3.1")
    patch("0003-Fix-clients-fftw3-include-dirs-rocm-4.5.patch", when="@4.5.0:5.1")
    # Patch to add install prefix header location for sqlite for 5.4
    patch("0004-fix-missing-sqlite-include-paths.patch", when="@5.4.0:5.4")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

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

    def cmake_args(self):
        args = [
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
        ]
        tgt = ROCmPackage.get_amdgpu_targets(self, spec)

        if "auto" not in tgt:
            if "@:3.8.0" in self.spec:
                args.append(
                    self.define(
                        "CMAKE_CXX_FLAGS", "--amdgpu-target={0}".format(",".join(tgt.value))
                    )
                )
            else:
                args.append(self.define("AMDGPU_TARGETS", tgt))

        # From version 3.9 and above we have AMDGPU_TARGETS_SRAM_ECC
        tgt_sram = ROCmPackage.get_amdgpu_targets_with_features(spec, "sramecc")

        if "auto" not in tgt_sram and self.spec.satisfies("@3.9.0:4.0.0"):
            args.append(
                self.define("AMDGPU_TARGETS_SRAM_ECC", tgt_sram)
            )

        # See https://github.com/ROCmSoftwarePlatform/rocFFT/issues/322
        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.0.0:"):
            args.append(self.define("SQLITE_USE_SYSTEM_PACKAGE", "ON"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args
