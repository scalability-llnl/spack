# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class Virtualgl(CMakePackage):
    """VirtualGL redirects 3D commands from a Unix/Linux OpenGL application
       onto a server-side GPU and converts the rendered 3D images into a video
       stream with which remote clients can interact to view and control the
       3D application in real time."""

    homepage = "http://www.virtualgl.org/Main/HomePage"
    url      = "http://downloads.sourceforge.net/project/virtualgl/2.5.2/VirtualGL-2.5.2.tar.gz"

    version('2.5.2', sha256='4f43387678b289a24139c5b7c3699740ca555a9f10011c979e51aa4df2b93238')

    # This package will only work with libjpeg-turbo, not other jpeg providers
    depends_on("libjpeg-turbo")
    depends_on("glu")
