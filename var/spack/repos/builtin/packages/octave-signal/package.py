# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveSignal(OctavePackage, SourceforgePackage):
    """Signal processing tools, including filtering, windowing and display functions."""

    homepage = "https://octave.sourceforge.io/optim/"
    sourceforge_mirror_path = "octave/signal-1.4.1.tar.gz"

    license("GPL-3.0-only")

    version("1.4.1", sha256="d978600f8b8f61339b986136c9862cad3e8f7015f84132f214bf63e9e281aeaa")

    depends_on("octave-control@2.4:")
    extends("octave@3.8.0:")
