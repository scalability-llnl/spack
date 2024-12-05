# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveIo(OctavePackage, SourceforgePackage):
    """The IO package is part of the Octave Forge project
    and provides input/output from/in external formats."""

    homepage = "https://octave.sourceforge.io/io/"
    sourceforge_mirror_path = "octave/io-2.6.3.tar.gz"

    license("GPL-3.0-only")

    version("2.6.3", sha256="6bc63c6498d79cada01a6c4446f793536e0bb416ddec2a5201dd8d741d459e10")
    version("2.6.2", sha256="01dbf8885a8011e76c919e271727c1d44f625bf6b217948b79438039ba368ceb")
    version("2.6.1", sha256="83253561f883c96ca3021a771223d23795122dc4cb800766e9cb893c6f8262dd")
    version("2.6.0", sha256="27f26273ced0b42c098e900136bb0ab2e542baf98d02bc0176cf47edbd0e6d7f")
    version("2.2.7", sha256="4eed2ee4c89b49ab160546c77ed66a384598f3bbb1c6e3833529c2c55aa479b6")

    extends("octave@4.2.0:")
