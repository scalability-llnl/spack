# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Irep(CMakePackage):
    """IREP is a tool that enables mixed-language simulation codes to use a
    common, Lua-based format for their input decks. Essentially, the input
    format is a set of tables -- Lua's one (and only?) data structure."""

    homepage = "https://irep.readthedocs.io/"
    url = "https://github.com/LLNL/irep/archive/refs/tags/v1.0.0.tar.gz"

    maintainers("tomstitt", "kennyweiss")

    license("MIT")

    version("1.0.0", sha256="b84203ac92de824dbdc672de45cfdb9609373791c4ee84a5201fa6e4ccecc1a4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("lua-lang")
