# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCssselect2(PythonPackage):
    """
    cssselect2 is a straightforward implementation of CSS4 Selectors for markup
    documents (HTML, XML, etc.) that can be read by ElementTree-like parsers
    (including cElementTree, lxml, html5lib, etc.)
    """

    homepage = "https://github.com/Kozea/cssselect2"
    pypi = "cssselect2/cssselect2-0.7.0.tar.gz"

    version("0.7.0", sha256="1ccd984dab89fc68955043aca4e1b03e0cf29cad9880f6e28e3ba7a74b14aa5a")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-tinycss2", type=("build", "run"))
    depends_on("py-webencodings", type=("build", "run"))
