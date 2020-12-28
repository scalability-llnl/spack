# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/coin-or/Osi/archive/releases/0.108.6.tar.gz"

    depends_on('coinutils')

    version('0.108.6', sha256='984a5886825e2da9bf44d8a665f4b92812f0700e451c12baf9883eaa2315fad5')

    build_directory = 'spack-build'
