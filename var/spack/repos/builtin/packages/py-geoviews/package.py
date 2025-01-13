# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeoviews(PythonPackage):
    """A Python library designed to make data analysis and visualization seamless and simple."""

    homepage = "https://geoviews.org/"
    pypi = "geoviews/geoviews-1.13.0.tar.gz"
    git = "https://github.com/holoviz/geoviews.git"

    license("BSD-3-Clause", checked_by="climbfuji")

    version("1.13.0", sha256="7554a1e9114995acd243546fac6c6c7f157fc28529fde6ab236a72a6e77fe0bf")
    # version("1.12.0", sha256="e2cbef0605e8fd1529bc643a31aeb61997f8f93c9b41a5aff8b2b355a76fa789")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")
    depends_on("py-bokeh@3.5", type=("build", "run"))

    depends_on("py-cartopy@0.18:", type="run")
    depends_on("py-holoviews@1.16:", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-packaging", type="run")
    depends_on("py-panel@1:", type="run")
    depends_on("py-param", type="run")
    depends_on("py-pyproj", type="run")
    depends_on("py-shapely", type="run")
    depends_on("py-xyzservices", type="run")
