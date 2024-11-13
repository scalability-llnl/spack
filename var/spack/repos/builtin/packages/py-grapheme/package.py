# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGrapheme(PythonPackage):
    """A Python package for working with user perceived characters. More
    specifically, string manipulation and calculation functions for working
    with grapheme cluster groups (graphemes) as defined by the
    Unicode Standard Annex #29."""

    homepage = "https://github.com/alvinlindstam/grapheme"
    pypi = "grapheme/grapheme-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="44c2b9f21bbe77cfb05835fec230bd435954275267fea1858013b102f8603cca")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
