# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Figcone(CMakePackage):
    """figcone - is a C++17 library, providing a convenient declarative interface for configuration
    parsers and built-in support for reading JSON, YAML, TOML, XML, INI and shoal config files."""

    homepage = "https://github.com/kamchatka-volcano/figcone"
    url = "https://github.com/kamchatka-volcano/figcone/archive/refs/tags/v2.4.9.tar.gz"

    license("MS-PL")

    version("3.0.0", sha256="24ed65c2dabc93b205c3adfdb5d7d0523286a956a0257dc5f15de91c5b828aea")
    version("2.4.9", sha256="735399e849621a4923e71a50d5e2ba928d5dfa3b01e54d56e0bac8e5102b7697")

    depends_on("cxx", type="build")  # generated
