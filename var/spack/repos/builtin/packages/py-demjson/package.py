# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDemjson(PythonPackage):
    """demjson is a Python language module for encoding, decoding, and syntax-checking JSON data"""

    homepage = "http://deron.meranda.us/python/demjson/"
    pypi = "demjson/demjson-2.2.4.tar.gz"

    license("LGPL-3.0-only")

    version("2.2.4", sha256="31de2038a0fdd9c4c11f8bf3b13fe77bc2a128307f965c8d5fb4dc6d6f6beb79")
    version("2.2.3", sha256="9fb0f3c02fe500104680af2889a64d1637b395aebdb37341ae2309d77854f40c")
    version("2.2.2", sha256="5114563dd3a0324b6c9c74250528660adbb6a095b2a015038149e31a9b5727d5")
    version("2.2.1", sha256="75055ebb6112a3c6bc3e009f528b209f9968773ebd3d3a1cd0d4b6c2006ee830")
    version("2.2", sha256="2aaa78c4d6f08c1bbcb88babd18cb54bb3ba2446870088ca33581c69f603a3a2")
    version("2.0.1", sha256="572c755df5aec7ac3fde5535795b8bf71f54e4681196c97a7a97d81916293504")
    version("2.0", sha256="24f638daa0c28a9d44db2282d46ea3edfd4c7d11a656e38677b741620bf1483d")
    version("1.6", sha256="1d989c310e33569ecc178b8182e53bde8f748bf5ea10cfbc0e331f8c313f6e29")
    version("1.5", sha256="446f4a74ba95679fa2fbe31887beb0c9870b6b8b2706ed5798bbf91339e8c349")
    version("1.4", sha256="e5858dc54a80290cecbc1d1514c6ce50dca44fbd15ccc195c4a8b6969b45a41f")

    depends_on("py-setuptools", type="build")
