# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Libdrm(MesonPackage):
    """A userspace library for accessing the DRM, direct rendering manager,
    on Linux, BSD and other systems supporting the ioctl interface."""

    homepage = "http://dri.freedesktop.org/libdrm/"
    url      = "https://dri.freedesktop.org/libdrm/libdrm-2.4.102.tar.xz"
    version('2.4.102', sha256='8bcbf9336c28e393d76c1f16d7e79e394a7fce8a2e929d52d3ad7ad8525ba05b')

    depends_on('pkgconfig', type='build')
    depends_on('libpciaccess@0.10:', when=(sys.platform != 'darwin'))
    depends_on('libpthread-stubs')

