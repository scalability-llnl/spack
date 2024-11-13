# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Osi(AutotoolsPackage):
    """Osi (Open Solver Interface) provides an abstract base class to
    a generic linear programming (LP) solver, along with derived
    classes for specific solvers. Many applications may be able to use
    the Osi to insulate themselves from a specific LP solver. That is,
    programs written to the OSI standard may be linked to any solver
    with an OSI interface and should produce correct results. The OSI
    has been significantly extended compared to its first
    incarnation. Currently, the OSI supports linear programming
    solvers and has rudimentary support for integer programming."""

    homepage = "https://projects.coin-or.org/Osi"
    url = "https://github.com/coin-or/Osi/archive/releases/0.108.6.tar.gz"

    depends_on("pkgconfig", type="build")
    depends_on("coinutils")
    depends_on("pkgconfig", type="build")

    license("EPL-2.0")

    version("0.108.8", sha256="8b01a49190cb260d4ce95aa7e3948a56c0917b106f138ec0a8544fadca71cf6a")
    version("0.108.7", sha256="f1bc53a498585f508d3f8d74792440a30a83c8bc934d0c8ecf8cd8bc0e486228")
    version("0.108.6", sha256="984a5886825e2da9bf44d8a665f4b92812f0700e451c12baf9883eaa2315fad5")

    depends_on("cxx", type="build")  # generated

    build_directory = "spack-build"
