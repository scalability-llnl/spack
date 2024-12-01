# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhanotate(PythonPackage):
    """PHANOTATE is a tool to annotate phage genomes. It uses the assumption
    that non-coding bases in a phage genome is disadvantageous, and then
    populates a weighted graph to find the optimal path through the six frames
    of the DNA where open reading frames are beneficial paths, while gaps and
    overlaps are penalized paths."""

    homepage = "https://github.com/deprekate/phanotate"
    pypi = "phanotate/phanotate-1.5.0.tar.gz"

    license("GPL-3.0-or-later")

    version("1.5.0", sha256="589e441d2369e5550aef98b8d99fd079d130363bf881a70ac862fc7a8e0d2c88")

    depends_on("c", type="build")  # generated

    depends_on("python@3.5.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-fastpath@1.3:", type=("build", "run"))
