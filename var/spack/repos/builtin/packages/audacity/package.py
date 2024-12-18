# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Audacity(CMakePackage):
    """Audacity is a cross-platform multitrack audio editor. It allows
    you to record sounds directly or to import files in various formats.
    It features a few simple effects, all of the editing features you
    should need, and unlimited undo. The GUI was built with wxWidgets
    and the audio I/O supports PulseAudio, OSS and ALSA under Linux."""

    homepage = "https://audacity.sourceforge.net"
    url = "https://github.com/audacity/audacity/archive/Audacity-2.4.2.tar.gz"

    license("GPL-3.0-or-later")

    version("2.4.2", sha256="cdb4800c8e9d1d4ca19964caf8d24000f80286ebd8a4db566c2622449744c099")
    version("2.4.1", sha256="50240f07471373a7e5c2df65cc26eeeaaced9a0850ad1f95cb795f171ea3009f")
    version("2.4.0", sha256="5d1c096d7b04ff8d5dbca3dca5b9d9f8e62093b5ea6e57ae5f821ae3132dc88f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("wxwidgets")
