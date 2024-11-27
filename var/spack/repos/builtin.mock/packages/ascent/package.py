# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ascent(Package):
    """This packagae has the variants shared, defaulted
    to True and adios2 defaulted to False"""

    homepage = "https://github.com/Alpine-DAV/ascent"
    url = "http://www.example.com/ascent-1.0.tar.gz"

    version("0.9.2", sha256="44cd954aa5db478ab40042cd54fd6fcedf25000c3bb510ca23fcff8090531b91")

    variant("adios2", default=False, description="Build Adios2 filter support")
    variant("shared", default=True, description="Build Ascent as shared libs")

    depends_on("adios2", when="+adios2")
