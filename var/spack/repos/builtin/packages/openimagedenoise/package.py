# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openimagedenoise(CMakePackage):
    """Intel Open Image Denoise is an open source library of high-performance,
    high-quality denoising filters for images rendered with ray tracing.
    Open Image Denoise is part of the Intel® oneAPI Rendering Toolkit and is released
    under the permissive Apache 2.0 license."""

    homepage = "https://www.openimagedenoise.org/"
    url = "https://github.com/RenderKit/oidn/releases/download/v1.4.3/oidn-1.4.3.src.tar.gz"

    license("Apache-2.0")

    version("2.3.0", sha256="cce3010962ec84e0ba1acd8c9055a3d8de402fedb1b463517cfeb920a276e427")
    version("2.2.2", sha256="d26b75fa216165086f65bf48c80648290f2cfed7d3c4bfc1e86c247b46c96b7e")
    version("2.1.0", sha256="ce144ba582ff36563d9442ee07fa2a4d249bc85aa93e5b25fc527ff4ee755ed6")
    version("2.0.1", sha256="328eeb9809d18e835dca7203224af3748578794784c026940c02eea09c695b90")
    version("1.4.3", sha256="3276e252297ebad67a999298d8f0c30cfb221e166b166ae5c955d88b94ad062a")
    version("1.4.2", sha256="e70d27ce24b41364782376c1b3b4f074f77310ccfe5f8ffec4a13a347e48a0ea")
    version("1.4.1", sha256="9088966685a78adf24b8de075d66e4c0019bd7b2b9d29c6e45aaf35d294e3f6f")
    version("1.4.0", sha256="3e7b85d344b3635719879c4444f061714e6e799895110bd5d78a357dc9b017db")
    version("1.3.0", sha256="88367b2bbea82d1df45d65141c36b6d86491bc6b397dc70beb3a05dda566f31c")
    version("1.2.4", sha256="948b070c780b5de0d983e7d5d37f6d9454932cc278913d9ee5b0bd047d23864a")
    version("1.2.3", sha256="469d20b093a73b18a54a2e559b0f18a6baac845ede864be62429737042ebe4f7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("ispc", type=("build"))
    depends_on("python@3:", type=("build", "test"))
    depends_on("tbb")

    def cmake_args(self):
        args = [self.define("OIDN_APPS", False)]
        return args
