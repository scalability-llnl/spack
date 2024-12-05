# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *
from spack.pkg.builtin.boost import Boost


class MiopenOpencl(CMakePackage):
    """AMD's library for high performance machine learning primitives."""

    homepage = "https://github.com/ROCm/MIOpen"
    git = "https://github.com/ROCm/MIOpen.git"
    url = "https://github.com/ROCm/MIOpen/archive/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libMIOpen"]

    license("MIT")

    version("5.5.1", sha256="2cd75071b8ee876c69a94f028b6c8a9346d6d2fde7d4b64e6d635f3b6c994262")
    version("5.5.0", sha256="791087242551669e546225e36123c21663f0dad14dbcfd6d0ce0e7bad0ab0de1")
    with default_args(deprecated=True):
        version("5.4.3", sha256="37ffe2ed3d7942da8ea2f6bdb85c7a2f58e3ccd31767db158a322769d3604efd")
        version("5.4.0", sha256="b4153791f9eeee4cbc5534bc6ad8b32c0947bcd38e08b77ebe144065a4fa5456")
        version("5.3.3", sha256="7efc98215d23a2caaf212378c37e9a6484f54a4ed3e9660719286e4f287d3715")
        version("5.3.0", sha256="c5819f593d71beeda2eb24b89182912240cc40f83b2b8f9de695a8e230aa4ea6")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5:", type="build")
    depends_on("boost@1.67.0:1.73.0", type="link")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type="link")
    depends_on("pkgconfig", type="build")
    depends_on("bzip2", type="link")
    depends_on("sqlite", type="link")
    depends_on("half", type="build")

    for ver in ["5.3.0", "5.3.3", "5.4.0", "5.4.3", "5.5.0", "5.5.1"]:
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"rocm-opencl@{ver}", when=f"@{ver}")
        depends_on(f"miopengemm@{ver}", when=f"@{ver}")

    for ver in ["5.3.0", "5.3.3"]:
        depends_on(f"mlirmiopen@{ver}", when=f"@{ver}")

    for ver in ["5.4.0", "5.4.3", "5.5.0", "5.5.1"]:
        depends_on("nlohmann-json", type="link")
        depends_on("rocblas", type="link")
        depends_on(f"rocmlir@{ver}", when=f"@{ver}")

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
        return [
            self.define("MIOPEN_BACKEND", "OpenCL"),
            self.define(
                "MIOPEN_HIP_COMPILER", "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix)
            ),
            self.define(
                "HIP_CXX_COMPILER", "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix)
            ),
            self.define(
                "MIOPEN_AMDGCN_ASSEMBLER", "{0}/bin/clang".format(self.spec["llvm-amdgpu"].prefix)
            ),
            self.define("Boost_USE_STATIC_LIBS", False),
        ]
