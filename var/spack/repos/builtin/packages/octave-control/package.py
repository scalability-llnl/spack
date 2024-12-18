# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveControl(OctavePackage, SourceforgePackage):
    """Computer-Aided Control System Design (CACSD) Tools for GNU Octave,
    based on the proven SLICOT Library"""

    homepage = "https://octave.sourceforge.io/control/"
    sourceforge_mirror_path = "octave/control-3.2.0.tar.gz"

    license("GPL-3.0-or-later")

    version("3.2.0", sha256="faf1d510d16ab46e4fa91a1288f4a7839ee05469c33e4698b7a007a0bb965e3e")

    depends_on("cxx", type="build")  # generated

    extends("octave@4.0.0:")
