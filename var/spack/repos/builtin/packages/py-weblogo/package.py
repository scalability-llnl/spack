# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWeblogo(PythonPackage):
    """WebLogo is a web based application designed to make the generation of
    sequence logos as easy and painless as possible."""

    homepage = "http://weblogo.threeplusone.com"
    pypi = "weblogo/weblogo-3.6.0.tar.gz"

    license("MIT")

    version("3.6.0", sha256="af5a9f065581f18d71bd7c22b160c1e443932f22cab992d439d3dc8757c80a85")
    version("3.5.0", sha256="84e39ee7c4f70efea55d6a92b3efdc4d2602b3d32a793f98865bca35e6bd1133")
    version("3.4", sha256="1fb661df47252064dd6d59d3c340b24d87bebe9048ca9ada904ac1e95669e08f")

    depends_on("py-setuptools", type="build")
    depends_on("ghostscript", type=("build", "run"))
    depends_on("pdf2svg", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
