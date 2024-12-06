# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskSphinxTheme(PythonPackage):
    """Sphinx theme for Dask documentation."""

    homepage = "https://github.com/dask/dask-sphinx-theme/"
    pypi = "dask_sphinx_theme/dask_sphinx_theme-1.3.5.tar.gz"

    license("BSD-3-Clause")

    version("1.3.5", sha256="151970cf0efedeb398fd6ca080407d3e81b4584d333e24498262d954171baa33")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx-rtd-theme", type=("build", "run"))
