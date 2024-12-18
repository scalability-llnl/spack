# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Scc(GoPackage):
    """
    Sloc, Cloc and Code: scc is a very fast accurate code counter with
    complexity calculations and COCOMO estimates written in pure Go.
    """

    homepage = "https://github.com/boyter/scc"
    url = "https://github.com/boyter/scc/archive/refs/tags/v3.1.0.tar.gz"
    git = "https://github.com/boyter/scc.git"

    license("MIT")

    version("3.4.0", sha256="bdedb6f32d1c3d73ac7e55780021c742bc8ed32f6fb878ee3e419f9acc76bdaa")
    version("3.3.2", sha256="2bbfed4cf34bbe50760217b479331cf256285335556a0597645b7250fb603388")
    version("3.1.0", sha256="bffea99c7f178bc48bfba3c64397d53a20a751dfc78221d347aabdce3422fd20")

    depends_on("go@1.20:", type="build", when="@3.2.0:")
    depends_on("go@1.22:", type="build", when="@3.4.0:")
