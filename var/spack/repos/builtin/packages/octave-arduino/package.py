# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveArduino(OctavePackage, SourceforgePackage):
    """Provides an Octave look-alike implementation of the
    Arduino extension for Matlab."""

    homepage = "https://octave.sourceforge.io/arduino/"
    sourceforge_mirror_path = "octave/arduino-0.2.0.tar.gz"

    license("GPL-3.0-or-later")

    version("0.2.0", sha256="0562ff48ea4b2cef28e2e03ccc4678dafa16f91d1580245bb7f9f488c4f56238")

    depends_on("cxx", type="build")  # generated

    depends_on("octave-instrctl")
    extends("octave@3.6.0:")
