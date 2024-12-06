# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BppSeqOmics(CMakePackage):
    """Bio++ Sequence Omics Library"""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/Installation"
    url = "https://github.com/BioPP/bpp-seq-omics/archive/v2.4.1.tar.gz"

    license("CECILL-2.0")

    version("2.4.1", sha256="200da925b42065998d825f0b2a37e26b00a865883c85bc332beb3a94cae1e08b")
    version("2.4.0", sha256="3217c7d6253f32c101d628aa039f2b3c49c3990de46c6842f2b88637da408e21")
    version("2.3.2", sha256="2254ffe181bb7582b73ca186cd366c321423177ea07866fd7c04c8a4bbcf5ac3")
    version("2.3.1", sha256="3217b35fa98e94824e19e5e2765f4561cb5d5ec0f93f5f4e7fc213e6b5b59e83")
    version("2.3.0", sha256="be0c8c593e48cd94a2a878e8635609788dfa806179f7844ecf8243e548bfe0fa")

    depends_on("cxx", type="build")  # generated

    depends_on("bpp-core")
    depends_on("bpp-seq")
