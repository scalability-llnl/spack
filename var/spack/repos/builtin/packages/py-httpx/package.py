# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpx(PythonPackage):
    """HTTPX is a fully featured HTTP client for Python 3, which provides sync
    and async APIs, and support for both HTTP/1.1 and HTTP/2."""

    homepage = "https://github.com/encode/httpx"
    pypi = "httpx/httpx-0.27.0.tar.gz"

    license("BSD-3-Clause")

    version("0.27.2", sha256="f7c2be1d2f3c3c3160d441802406b206c2b76f5947b11115e6df10c6c65e66c2")
    version("0.27.0", sha256="a0cb88a46f32dc874e04ee956e4c2764aba2aa228f650b06788ba6bda2962ab5")
    version("0.23.3", sha256="9818458eb565bb54898ccb9b8b251a28785dd4a55afbc23d0eb410754fe7d0f9")
    version("0.22.0", sha256="d8e778f76d9bbd46af49e7f062467e3157a5a3d2ae4876a4bbfd8a51ed9c9cb4")
    version("0.15.2", sha256="713a2deaf96d85bbd4a1fbdf0edb27d6b4ee2c9aaeda8433042367e4b9e1628d")
    version("0.11.1", sha256="7d2bfb726eeed717953d15dddb22da9c2fcf48a4d70ba1456aa0a7faeda33cf7")

    variant("http2", default=False, when="@0.15.2:", description="Enable http2 support")

    depends_on("python@3.8:", when="@0.27:", type=("build", "run"))
    depends_on("py-setuptools", when="@:0.22", type="build")
    depends_on("py-hatchling", when="@0.23:", type="build")
    depends_on("py-hatch-fancy-pypi-readme", when="@0.23:", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-certifi")

        depends_on("py-httpcore@0.11", when="@0.15.2")
        depends_on("py-httpcore@0.14.5:0.14", when="@0.22")
        depends_on("py-httpcore@0.15:0.16", when="@0.23")
        depends_on("py-httpcore@1", when="@0.27:")

        depends_on("py-anyio", when="@0.27:")
        depends_on("py-idna", when="@0.27:")

        depends_on("py-sniffio@1", when="@0.11.1")
        depends_on("py-sniffio", when="@0.15.2:")

        depends_on("py-h2@3", when="@0.11.1")
        depends_on("py-h2@3", when="@0.15.2+http2")
        depends_on("py-h2@3:4", when="@0.22.0:+http2")

        # Historical dependencies
        depends_on("py-hstspreload", when="@0.11.1")
        depends_on("py-chardet@3", when="@0.11.1")
        depends_on("py-h11@0.8:0.9", when="@0.11.1")
        depends_on("py-idna@2", when="@0.11.1")
        depends_on("py-urllib3@1", when="@0.11.1")
        depends_on("py-charset-normalizer", when="@0.22")

        depends_on("py-rfc3986@1.3:1", when="@0.11.1")
        depends_on("py-rfc3986+idna2008@1.3:1", when="@0.15.2:2.23.3")
