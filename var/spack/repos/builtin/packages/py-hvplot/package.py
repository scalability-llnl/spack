# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHvplot(PythonPackage):
    """A high-level plotting API for pandas, dask, xarray, and networkx built on HoloViews."""

    homepage = "https://hvplot.holoviz.org/"
    pypi = "hvplot/hvplot-1.19.1.tar.gz"
    git = "http://github.com/holoviz/hvplot.git"

    license("BSD-3-Clause", checked_by="climbfuji")

    version("0.11.1", sha256="989ed0389189adc47edcd2601d2eab18bf366e74b07f5e2873e021323c4a14bb")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@30.3:", type="build")
    depends_on("py-setuptools-scm@6:", type="build")

    depends_on("py-bokeh@3.1:", type="run")
    depends_on("py-colorcet", type="run")
    depends_on("py-holoviews@1.19:", type="run")
    depends_on("py-numpy@1.21:", type="run")
    depends_on("py-packaging", type="run")
    depends_on("py-pandas@1.3:", type="run")
    depends_on("py-panel@1:", type="run")
    depends_on("py-param@1.12:2", type="run")
