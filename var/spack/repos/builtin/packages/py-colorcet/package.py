# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyColorcet(PythonPackage):
    """A collection of perceptually acccurate 256-color colormaps for use with
    Python plotting programs like Bokeh, Matplotlib, HoloViews, and Datashader."""

    homepage = "https://colorcet.holoviz.org/index.html"
    pypi = "colorcet/colorcet-3.0.0.tar.gz"

    maintainers("vvolkl")

    version("3.0.0", sha256="21c522346a7aa81a603729f2996c22ac3f7822f4c8c303c59761e27d2dfcf3db")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools@30.3.0:", type="build")
    depends_on("py-param@1.7.0:", type=("build", "run"))
    depends_on("py-pyct@0.4.4:", type=("build", "run"))
