# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Raptor2(AutotoolsPackage):
    """libraptor2 for parsing and serializing RDF syntaxes"""

    homepage = "https://librdf.org/"
    url = "https://download.librdf.org/source/raptor2-2.0.15.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.0.16", sha256="089db78d7ac982354bdbf39d973baf09581e6904ac4c92a98c5caadb3de44680")
    version("2.0.15", sha256="ada7f0ba54787b33485d090d3d2680533520cd4426d2f7fb4782dd4a6a1480ed")

    depends_on("c", type="build")  # generated

    depends_on("libxml2")
