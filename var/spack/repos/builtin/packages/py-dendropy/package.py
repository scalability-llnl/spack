# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDendropy(PythonPackage):
    """DendroPy is a Python library for phylogenetic computing. It provides
    classes and functions for the simulation, processing, and manipulation of
    phylogenetic trees and character matrices, and supports the reading and
    writing of phylogenetic data in a range of formats, such as NEXUS, NEWICK,
    NeXML, Phylip, FASTA, etc."""

    homepage = "https://www.dendropy.org"
    pypi = "dendropy/DendroPy-4.3.0.tar.gz"

    license("CC-BY-NC-SA-4.0")

    version("4.5.2", sha256="3e5d2522170058ebc8d1ee63a7f2d25b915e34957dc02693ebfdc15f347a0101")
    version("4.3.0", sha256="bd5b35ce1a1c9253209b7b5f3939ac22beaa70e787f8129149b4f7ffe865d510")
    version("3.12.0", sha256="38a0f36f2f7aae43ec5599408b0d0a4c80996b749589f025940d955a70fc82d4")

    depends_on("python@2.7:,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
