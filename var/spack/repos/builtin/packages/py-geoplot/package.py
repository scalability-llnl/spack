# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeoplot(PythonPackage):
    """geoplot is a high-level Python geospatial plotting library.

    It's an extension to cartopy and matplotlib which makes mapping easy:
    like seaborn for geospatial."""

    homepage = "https://github.com/ResidentMario/geoplot"
    pypi = "geoplot/geoplot-0.4.1.tar.gz"

    maintainers("adamjstewart")

    version("0.4.1", sha256="eb073436c5a1cb7f97caa217cdb109e6cad4f3774e657757005e3f0f5a3183ca")

    depends_on("python@3.6.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-geopandas", type=("build", "run"))
    depends_on("py-cartopy", type=("build", "run"))
    depends_on("py-descartes", type=("build", "run"))
    depends_on("py-mapclassify@2.1:", type=("build", "run"))
    depends_on("py-contextily@1.0.0:", type=("build", "run"))
