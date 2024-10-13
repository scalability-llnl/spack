# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGleanSdk(PythonPackage):
    """Mozilla's Glean Telemetry SDK"""

    homepage = "https://mozilla.github.io/glean/book/index.html"
    url = "https://github.com/mozilla/glean/archive/refs/tags/v60.4.0.tar.gz"

    license("MPL-2.0", checked_by="teaguesterling")

    version("60.5.0", sha256="0a23adad449c05d2cc522dc28ef98287b59a42ff112e53e3c8b4cfe9c938f6ae")
    version("60.4.0", sha256="24bc608e06580962ce029cc4c09a51af75e4a29b3d889232b298f87208acbf62")
    version("60.0.1", sha256="ba7fb8b1e4ecd50da4dc2e02ef887a71d93f848580e17a6f3e947ed3bcf68726")

    depends_on("python@3.8:")
    depends_on("py-semver@2.13.0:")
    depends_on("py-glean-parser@14.0", when="@:60.3")
    depends_on("py-glean-parser@14.3:", when="@60.4:")
    depends_on("py-maturin@1")
