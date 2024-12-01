# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Findbugs(Package):
    """a program which uses static analysis to look for bugs in Java code.
    It is free software, distributed under the terms of the Lesser GNU
    Public License."""

    homepage = "https://findbugs.sourceforge.net/"
    url = "https://sourceforge.net/projects/findbugs/files/findbugs/3.0.1/findbugs-3.0.1.tar.gz"
    list_url = "https://sourceforge.net/projects/findbugs/files/findbugs"
    list_depth = 1

    version("3.0.1", sha256="e80e0da0c213a27504ef3188ef25f107651700ffc66433eac6a7454bbe336419")
    version("3.0.0", sha256="31c75797ead68dbb334fd57bf16f4b7b99c9e266447171453e06fdf673335f33")
    version("2.0.3", sha256="59ba2a64d786ae5b3fa46e9f9c7bb3ea91c24d43d383c8ef594217f6f51e499f")

    depends_on("java", type=("run"))

    def install(self, spec, prefix):
        install_tree(".", prefix)
