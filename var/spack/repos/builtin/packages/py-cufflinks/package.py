# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCufflinks(PythonPackage):
    """Productivity Tools for Plotly + Pandas. This library binds the power
    of plotly with the flexibility of pandas for easy plotting."""

    homepage = "https://github.com/santosjorge/cufflinks"
    pypi = "cufflinks/cufflinks-0.17.3.tar.gz"

    license("MIT")

    version("0.17.3", sha256="48c1b3406dc030004121966489eebc5518cea70fd4e3f16379b491328501a644")

    depends_on("py-setuptools@34.4.1:", type=("build", "run"))
    depends_on("py-numpy@1.9.2:", type=("build", "run"))
    depends_on("py-pandas@0.19.2:", type=("build", "run"))
    depends_on("py-plotly@4.1.1:", type=("build", "run"))
    depends_on("py-six@1.9.0:", type=("build", "run"))
    depends_on("py-colorlover@0.2.1:", type=("build", "run"))
    depends_on("py-ipython@5.3.0:", type=("build", "run"))
    depends_on("py-ipywidgets@7.0.0:", type=("build", "run"))
