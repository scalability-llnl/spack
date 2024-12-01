# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCairosvg(PythonPackage):
    """
    CairoSVG is an SVG converter based on Cairo.
    It can export SVG files to PDF, EPS, PS, and PNG files.
    """

    homepage = "https://cairosvg.org/"
    pypi = "CairoSVG/CairoSVG-2.7.1.tar.gz"

    version("2.7.1", sha256="432531d72347291b9a9ebfb6777026b607563fd8719c46ee742db0aef7271ba0")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cairocffi", type=("build", "run"))
    depends_on("py-cssselect2", type=("build", "run"))
    depends_on("py-defusedxml", type=("build", "run"))
    depends_on("py-pillow", type=("build", "run"))
    depends_on("py-tinycss2", type=("build", "run"))
