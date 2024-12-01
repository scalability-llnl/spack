# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libinih(MesonPackage):
    """
    inih (INI Not Invented Here) is a simple .INI file parser written in C.
    """

    homepage = "https://github.com/benhoyt/inih"
    url = "https://github.com/benhoyt/inih/archive/refs/tags/r53.tar.gz"
    git = "https://github.com/benhoyt/inih.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
