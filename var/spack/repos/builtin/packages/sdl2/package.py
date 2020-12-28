# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sdl2(CMakePackage):
    """Simple DirectMedia Layer is a cross-platform development library
    designed to provide low level access to audio, keyboard, mouse, joystick,
    and graphics hardware via OpenGL and Direct3D."""

    homepage = "https://wiki.libsdl.org/FrontPage"
    url      = "https://libsdl.org/release/SDL2-2.0.5.tar.gz"

    version('2.0.5', sha256='442038cf55965969f2ff06d976031813de643af9c9edc9e331bd761c242e8785')

    depends_on('cmake@2.8.5:', type='build')
    depends_on('libxext', type='link')

    def cmake_args(self):
        return [
            '-DSSEMATH={0}'.format(
                'OFF' if self.spec.target.family == 'aarch64' else 'ON'
            )
        ]
