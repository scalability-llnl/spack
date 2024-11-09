# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dotconf(AutotoolsPackage):
    """dot.conf configuration file parser."""

    homepage = "https://github.com/williamh/dotconf"
    url = "https://github.com/williamh/dotconf/archive/v1.3.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.3", sha256="7f1ecf40de1ad002a065a321582ed34f8c14242309c3547ad59710ae3c805653")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
