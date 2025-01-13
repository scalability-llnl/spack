# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHoloviews(PythonPackage):
    """A Python library designed to make data analysis and visualization seamless and simple."""

    homepage = "https://holoviews.org/"
    pypi = "holoviews/holoviews-1.19.1.tar.gz"
    git = "https://github.com/holoviz/holoviews.git"

    license("BSD-3-Clause", checked_by="climbfuji")

    version("1.19.1", sha256="b9e85e8c07275a456c0ef8d06bc157d02b37eff66fb3602aa12f5c86f084865c")
    # version("1.19.0", sha256="cab1522f75a9b46377f9364b675befd79812e220059714470a58e21475d531ba")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-bokeh@3.1:", type="run")
    depends_on("py-colorcet", type="run")
    depends_on("py-numpy@1.21:", type="run")
    depends_on("py-packaging", type="run")
    depends_on("py-pandas@1.3:", type="run")
    depends_on("py-panel@1:", type="run")
    depends_on("py-param@2", type="run")
    depends_on("py-pyviz-comms@2.1:", type="run")
