# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# ----------------------------------------------------------------------------

from spack.package import *


class PyPykokkosBase(CMakePackage, PythonExtension):
    """Minimal set of bindings for Kokkos interoperability with Python
    (initialize, finalize, View, DynRankView, Kokkos-tools)"""

    homepage = "https://github.com/kokkos/pykokkos-base.git"
    git = "https://github.com/kokkos/pykokkos-base.git"
    maintainers("jrmadsen")

    version("main", branch="main", submodules=False)
    version("0.0.5", commit="45f6e892c007ab124fabb3a545f4744537eafb55", submodules=False)
    version("0.0.4", commit="2efe1220d0128d3f2d371c9ed5234c4978d73a77", submodules=False)
    version("0.0.3", commit="4fe4421ac624ba2efe1eee265153e690622a18a5", submodules=False)

    depends_on("cxx", type="build")  # generated

    variant(
        "layouts", default=True, description="Build Kokkos View/DynRankView with layout variants"
    )
    variant(
        "memory_traits",
        default=True,
        description="Build Kokkos View/DynRankView with memory trait variants",
    )
    variant(
        "view_ranks",
        default="4",
        description="Max Kokkos View dimensions",
        values=("1", "2", "3", "4", "5", "6", "7"),
        multi=False,
    )

    extends("python")
    depends_on("cmake@3.16:", type="build")
    depends_on("py-pybind11", type="build")
    depends_on("kokkos@3.4.00:", type=("build", "run"))
    depends_on("python@3:", type=("build", "run"))

    def cmake_args(self):
        args = [
            self.define("ENABLE_INTERNAL_KOKKOS", False),
            self.define("ENABLE_INTERNAL_PYBIND11", False),
            self.define_from_variant("ENABLE_VIEW_RANKS", "view_ranks"),
        ]

        for dep in ("layouts", "memory_traits"):
            args.append(self.define_from_variant("ENABLE_" + dep.upper(), dep))

        return args
