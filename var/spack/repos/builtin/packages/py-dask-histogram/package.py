# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskHistogram(PythonPackage):
    """Histograms with task scheduling."""

    homepage = "https://github.com/dask-contrib/dask-histogram"
    pypi = "dask_histogram/dask_histogram-2024.3.0.tar.gz"

    maintainers("wdconinc")

    license("BSD-3-Clause", checked_by="wdconinc")

    version("2024.3.0", sha256="834d4d25f5e2c417f5e792fafaa55484c20c9f3812d175125de7ac34f994ef7b")

    depends_on("py-hatchling@1.8.0:", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-boost-histogram@1.3.2:", type=("build", "run"))
    depends_on("py-dask@2021.03.0:", type=("build", "run"))
