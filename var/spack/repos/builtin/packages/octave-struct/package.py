# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveStruct(OctavePackage, SourceforgePackage):
    """Additional structure manipulation functions for Octave."""

    homepage = "https://octave.sourceforge.io/struct/"
    sourceforge_mirror_path = "octave/struct-1.0.14.tar.gz"

    license("GPL-3.0-only")

    version("1.0.17", sha256="0137bbb5df650f29104f6243502f3a2302aaaa5e42ea9f02d8a3943aaf668433")
    version("1.0.14", sha256="ad4e17687bc24650f032757271b20b70fe32c35513d4dd9ab1e549919df36b47")
    extends("octave@2.9.7:")
