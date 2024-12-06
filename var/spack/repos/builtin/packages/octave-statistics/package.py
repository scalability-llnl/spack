# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveStatistics(OctavePackage, SourceforgePackage):
    """Additional statistics functions for Octave."""

    homepage = "https://octave.sourceforge.io/statistics/"
    sourceforge_mirror_path = "octave/statistics-1.4.2.tar.gz"

    version("1.4.2", sha256="7976814f837508e70367548bfb0a6d30aa9e447d4e3a66914d069efb07876247")

    depends_on("octave-io")
    extends("octave@4.0.0:")
