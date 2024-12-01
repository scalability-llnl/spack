# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCharsetNormalizer(PythonPackage):
    """The Real First Universal Charset Detector. Open, modern and actively
    maintained alternative to Chardet."""

    homepage = "https://github.com/ousret/charset_normalizer"
    pypi = "charset-normalizer/charset-normalizer-2.0.7.tar.gz"

    license("MIT")

    version("3.3.0", sha256="63563193aec44bce707e0c5ca64ff69fa72ed7cf34ce6e11d5127555756fd2f6")
    version("3.1.0", sha256="34e0a2f9c370eb95597aae63bf85eb5e96826d81e3dcf88b8886012906f509b5")
    version("2.1.1", sha256="5a3d016c7c547f69d6f81fb0db9449ce888b418b5b9952cc5e6e66843e9dd845")
    version("2.0.12", sha256="2857e29ff0d34db842cd7ca3230549d1a697f96ee6d3fb071cfa6c7393832597")
    version("2.0.7", sha256="e019de665e2bcf9c2b64e2e5aa025fa991da8720daa3c1138cadd2fd1856aed0")

    depends_on("py-setuptools", type="build")
