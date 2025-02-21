# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
