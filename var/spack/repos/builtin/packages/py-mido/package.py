# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMido(PythonPackage):
    """Mido is a library for working with MIDI messages and ports. It's
    designed to be as straight forward and Pythonic as possible."""

    homepage = "https://mido.readthedocs.io/"
    url = "https://github.com/mido/mido/archive/1.2.9.tar.gz"

    license("MIT")

    version("1.2.9", sha256="6d68d7514bb3320f505ba4d7e06006c4725c0b97f281126bc983f3f7eeed697a")
    version("1.2.8", sha256="4d26706430ea87dfcd950b19979d3edb97b2b113eb7e233c64290713cf7ec7b9")
    version("1.2.7", sha256="7fb8d2c4b16b1d4f18b2e440654905ad63a8d24121f41b0126f39e3c7db89cf1")
    version("1.2.6", sha256="870d2f470ce1123324f9ef9676b6c9f2580293dd2a07fdfe00e20a47740e8b8e")

    depends_on("py-setuptools", type="build")
