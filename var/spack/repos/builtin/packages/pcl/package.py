# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Pcl(CMakePackage):
    """The Point Cloud Library (PCL) is a standalone, large scale,
    open project for 2D/3D image and point cloud processing."""

    homepage = "https://pointclouds.org/"
    url      = "https://github.com/PointCloudLibrary/pcl/releases/download/pcl-1.11.1/source.tar.gz"

    version('1.11.1', sha256='19d1a0bee2bc153de47c05da54fc6feb23393f306ab2dea2e25419654000336e')

    depends_on('cmake@3.5:', type='build')
    depends_on('eigen@3.1:')
    depends_on('flann@1.7:')
    depends_on('boost@1.55:+filesystem+date_time+iostreams+system')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
