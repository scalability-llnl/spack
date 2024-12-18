# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Miopengemm(CMakePackage):
    """An OpenCL general matrix multiplication (GEMM) API
    and kernel generator"""

    homepage = "https://github.com/ROCm/MIOpenGEMM"
    git = "https://github.com/ROCm/MIOpenGEMM.git"
    url = "https://github.com/ROCm/MIOpenGEMM/archive/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libmiopengemm"]

    def url_for_version(self, version):
        if version == Version("1.1.6"):
            return "https://github.com/ROCm/MIOpenGEMM/archive/1.1.6.tar.gz"
        url = "https://github.com/ROCm/MIOpenGEMM/archive/rocm-{0}.tar.gz"
        return url.format(version)

    license("MIT")

    version("5.5.1", sha256="a997b560521641e7173613cf547ecde5d15ac6fac1786d392b0f133c91f99a40")
    version("5.5.0", sha256="ffd9775129564662b338952588057a088f7e9723b4a9a766b2dd96fdc0992c26")
    with default_args(deprecated=True):
        version("5.4.3", sha256="5051051cab60ca0f6347a981da6c9dbeddf8b0de698d4e5409a0db0c622acafc")
        version("5.4.0", sha256="a39faa8f4ab73e0cd6505a667bf10c07f93b9612af0711405c65043c4755129d")
        version("5.3.3", sha256="4a9c92bebe59bf6e08bd48861b68b1801d9e8dc406250dc8637d36614a5884c8")
        version("5.3.0", sha256="7e299daaca8e514bdb5b5efd9d9d3fc5cbfda68ad0117fe7cdbbf946b3f842cd")
        version("5.2.3", sha256="de9eecf39e6620be1511923e990101e64c63c2f56d8491c8bf9ffd1033709c00")
        version("5.2.1", sha256="9cea190ee0a6645b6d3ce3e136a8e7d07cf4044e98014ccc82b5e5f8b468b1c1")
        version("5.2.0", sha256="10458fb07b56a7fbe165595d588b7bf5f1300c57bda2f3133c3687c7bae39ea8")
        version("5.1.3", sha256="c70fc9e2a6d47356a612e24f5757bf16fdf26e671bd53a0975c1a0978da740b6")
        version("5.1.0", sha256="e2b20cdc20a745bcb7a554852e6b4bd39274c7dcc13fc19a81a282fb4dfa475f")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3:", type="build")

    for ver in ["5.3.0", "5.3.3", "5.4.0", "5.4.3", "5.5.0", "5.5.1"]:
        depends_on(f"rocm-cmake@{ver}", type="build", when=f"@{ver}")
        depends_on(f"rocm-opencl@{ver}", when=f"@{ver}")

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
