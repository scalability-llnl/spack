# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyani(PythonPackage):
    """pyani is a Python3 module that provides support for calculating
    average nucleotide identity (ANI) and related measures for whole genome
    comparisons, and rendering relevant graphical summary output. Where
    available, it takes advantage of multicore systems, and can integrate
    with SGE/OGE-type job schedulers for the sequence comparisons."""

    homepage = "https://widdowquinn.github.io/pyani"
    pypi = "pyani/pyani-0.2.7.tar.gz"

    license("MIT")

    version("0.2.7", sha256="dbc6c71c46fbbfeced3f8237b84474221268b51170caf044bec8559987a7deb9")
    version("0.2.6", sha256="e9d899bccfefaabe7bfa17d48eef9c713d321d2d15465f7328c8984807c3dd8d")

    depends_on("python@3.5:")
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))

    # Required for ANI analysis
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

    # Required for ANIb analysis
    depends_on("blast-plus~python", type="run")

    # Required for ANIm analysis
    depends_on("mummer", type="run")
