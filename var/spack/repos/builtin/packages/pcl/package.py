# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    version("1.13.1", sha256="be4d499c066203a3c296e2f7e823d6209be5983415f2279310ed1c9abb361d30")
    version("1.13.0", sha256="bd110789f6a7416ed1c58da302afbdb80f8d297a9e23cc02fd78ab78b4762698")
    version("1.12.1", sha256="a9573efad5e024c02f2cc9180bb8f82605c3772c62463efbe25c5d6e634b91dc")
    version("1.12.0", sha256="606a2d5c7af304791731d6b8ea79365bc8f2cd75908006484d71ecee01d9b51c")
    version("1.11.1", sha256="19d1a0bee2bc153de47c05da54fc6feb23393f306ab2dea2e25419654000336e")

    depends_on("cmake@3.5:", type="build")
    depends_on("eigen@3.1:")
    depends_on("flann@1.7:")
    depends_on("boost@1.55:+filesystem+date_time+iostreams+system")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
