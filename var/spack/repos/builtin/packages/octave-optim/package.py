# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveOptim(OctavePackage, SourceforgePackage):
    """Non-linear optimization toolkit for Octave."""

    homepage = "https://octave.sourceforge.io/optim/"
    sourceforge_mirror_path = "octave/optim-1.5.2.tar.gz"

    version('1.5.2', sha256='7b36033c5581559dc3e7616f97d402bc44dde0dfd74c0e3afdf47d452a76dddf')

    depends_on('octave-struct@1.0.12:')
    extends('octave@3.6.0:')
