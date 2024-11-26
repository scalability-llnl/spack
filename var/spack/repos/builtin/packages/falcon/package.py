# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Falcon(PythonPackage):
    """Falcon: a set of tools for fast aligning long reads for consensus
    and assembly.

    The Falcon tool kit is a set of simple code collection which I use
    for studying efficient assembly algorithm for haploid and diploid genomes.
    It has some back-end code implemented in C for speed and some simple
    front-end written in Python for convenience."""

    homepage = "https://github.com/PacificBiosciences/FALCON"
    git = "https://github.com/PacificBiosciences/FALCON.git"

    version("2017-05-30", commit="86cec6157291679095ea6080b0cde6561eccc041")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="run")
    depends_on("py-pypeflow", type="run")
    depends_on("py-networkx@1.7:1.10", type=["build", "run"])
    depends_on("pacbio-dazz-db", type="run")
    depends_on("pacbio-daligner", type="run")
    depends_on("pacbio-dextractor", type="run")
    depends_on("pacbio-damasker", type="run")

    # Python version 3 and later should return
    # a value of PyObject type. [-Wreturn-type]
    patch("Py_None.patch", when="^python@3:")
