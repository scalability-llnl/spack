# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Transposome(PerlPackage):
    """A toolkit for annotation of transposable element families from
    unassembled sequence reads."""

    homepage = "https://sestaton.github.io/Transposome/"
    url = "https://github.com/sestaton/Transposome/archive/v0.11.2.tar.gz"

    version("0.12.1", sha256="fc3706a883cba58626ccd753df7a77f0baf52ff3b1d8aa7644a7f474f296a603")
    version("0.11.2", sha256="f0bfdb33c34ada726b36c7b7ed6defa8540a7f8abe08ad46b3ccfec5dcd4720d")

    depends_on("cxx", type="build")  # generated

    depends_on("blast-plus")
