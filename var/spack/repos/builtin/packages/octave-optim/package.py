# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveOptim(OctavePackage, SourceforgePackage):
    """Non-linear optimization toolkit for Octave."""

    homepage = "https://octave.sourceforge.io/optim/"
    sourceforge_mirror_path = "octave/optim-1.5.2.tar.gz"

    version("1.6.1", sha256="7150cdfac7e9da31ec7ac1cfe8619d9c0e9c8b3f787f54bf89e0fb1c275be584")
    version("1.5.2", sha256="7b36033c5581559dc3e7616f97d402bc44dde0dfd74c0e3afdf47d452a76dddf")

    depends_on("octave-struct@1.0.12:")
    depends_on("octave-statistics@1.4.0:")
    extends("octave@3.6.0:", when="@:1.5.2")
    extends("octave@4.0.0:", when="@1.6.1:")
