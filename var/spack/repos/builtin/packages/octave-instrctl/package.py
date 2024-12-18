# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveInstrctl(OctavePackage, SourceforgePackage):
    """Instrument-Control is a package for interfacing the outside world of hardware
    via Serial, i2c or Parallel interfaces."""

    homepage = "https://octave.sourceforge.io/instrument-control/"
    sourceforge_mirror_path = "octave/instrument-control-0.3.1.tar.gz"

    version("0.3.1", sha256="d9c3b2e258cc8245ebfdd282e6314af12987daf453f4356555f56ca5ec55873c")

    depends_on("cxx", type="build")  # generated

    extends("octave@3.6.0:")
