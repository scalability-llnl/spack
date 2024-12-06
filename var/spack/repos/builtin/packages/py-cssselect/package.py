# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCssselect(PythonPackage):
    """Python-cssselect parses CSS3 Selectors and translate them to XPath 1.0
    expressions. Such expressions can be used in lxml or another XPath engine
    to find the matching elements in an XML or HTML document."""

    homepage = "https://github.com/scrapy/cssselect"
    url = "https://github.com/scrapy/cssselect/archive/v1.1.0.tar.gz"

    license("BSD-3-Clause")

    version("1.1.0", sha256="dde8c1d4a2c82de6889a3af1c1adbce1a6f3ec08b07a854d873f3f3da92960af")
    version("1.0.3", sha256="203d9691c42c13cffe26a2f8fc714977882fcf54a6df82c8eda3371f6beaecdb")
    version("1.0.2", sha256="ee16bbb99b0a1f593ed4cd822f20bffefa4a4676d19d7dd1f231b4c1cc1cc1e2")
    version("1.0.1", sha256="cdfa17ab5dc8818209f310a930b18d3035a4585ddd2c179e833036e2dde511c6")
    version("1.0.0", sha256="2f757203e03aedcc1b31a452cf2752728b843351b7819ea2d4cd9ef38df7b324")

    depends_on("py-setuptools", type="build")
