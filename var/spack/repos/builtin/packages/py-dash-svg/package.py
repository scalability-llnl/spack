# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDashSvg(PythonPackage):
    """SVG support library for Plotly/Dash"""

    homepage = "https://github.com/stevej2608/dash-svg"
    pypi = "dash_svg/dash_svg-0.0.12.tar.gz"

    license("MIT")

    version("0.0.12", sha256="a7115bf437d770b822c2dd53b9d9a981210619b7d17c925cbee04905fc761b4e")

    depends_on("py-setuptools", type="build")
