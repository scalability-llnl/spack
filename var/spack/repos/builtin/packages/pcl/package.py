# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Pcl(CMakePackage):
    """The Point Cloud Library (PCL) is a standalone, large scale,
    open project for 2D/3D image and point cloud processing."""

    homepage = "https://pointclouds.org/"
    url = "https://github.com/PointCloudLibrary/pcl/releases/download/pcl-1.11.1/source.tar.gz"

    license("BSD-3-Clause")

    version("1.14.1", sha256="cc3dc26a9ea176cb588fb1f182324399dbaf11e5ba1bea95c7d39005b7a5d352")
    version("1.13.1", sha256="be4d499c066203a3c296e2f7e823d6209be5983415f2279310ed1c9abb361d30")
    version("1.13.0", sha256="bd110789f6a7416ed1c58da302afbdb80f8d297a9e23cc02fd78ab78b4762698")
    version("1.12.1", sha256="a9573efad5e024c02f2cc9180bb8f82605c3772c62463efbe25c5d6e634b91dc")
    version("1.12.0", sha256="606a2d5c7af304791731d6b8ea79365bc8f2cd75908006484d71ecee01d9b51c")
    version("1.11.1", sha256="19d1a0bee2bc153de47c05da54fc6feb23393f306ab2dea2e25419654000336e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5:", type="build")
    depends_on("cmake@3.10:", when="@1.12.1:", type="build")
    depends_on("eigen@3.1:")
    depends_on("eigen@3.3:", when="@1.13:")
    depends_on("flann@1.7:")
    depends_on("flann@1.9.1:", when="@1.12:")
    depends_on("boost@1.55:")
    depends_on("boost@1.65:", when="@1.12:")
    depends_on("boost+filesystem+iostreams+system")
    depends_on("boost+date_time", when="@:1.13.0")

    # fix build with clang: #30653
    with when("@:1.12"):
        patch(
            "https://github.com/PointCloudLibrary/pcl/commit/dff16af269fbd2c15772d53064882b2bf8c2ffe9.patch?full_index=1",
            sha256="17a7a7aec8e63701294612cbb25d46ac1ce58f643dbc68e1517329ae0b68956d",
        )

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
