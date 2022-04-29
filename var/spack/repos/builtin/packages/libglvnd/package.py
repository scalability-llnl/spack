# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Libglvnd(AutotoolsPackage):
    """The GL Vendor-Neutral Dispatch library
    libglvnd is a vendor-neutral dispatch layer for arbitrating OpenGL API
    calls between multiple vendors. It allows multiple drivers from different
    vendors to coexist on the same filesystem, and determines which vendor to
    dispatch each API call to at runtime.
    Both GLX and EGL are supported, in any combination with OpenGL and OpenGL
    ES.

    The codependency between libglvnd and the underlying implementation is modeled
    in Spack with two packages for libglvnd: libglvnd, which provides libglvnd
    proper; and libglvnd-fe, a bundle package that depends on libglvnd and an
    implementation.  Implementations that work through libglvnd are no longer
    providers for graphics virtual dependencies, like "gl" or "glx", but instead
    provide libglvnd versions of these dependencies ("libglvnd-be-gl",
    "libglvnd-be-glx", etc.).  The libglvnd-fe package depends on these
    "libglvnd-be-..." virtual packages, which provide the actual implementation.
    It also depends on libglvnd, itself, and exposes its libraries to downstream
    applications."""

    homepage = "https://gitlab.freedesktop.org/glvnd/libglvnd"
    url      = "https://gitlab.freedesktop.org/glvnd/libglvnd/-/archive/v1.0.0/libglvnd-v1.0.0.tar.bz2"
    git      = "https://gitlab.freedesktop.org/glvnd/libglvnd.git"

    version('master', branch='master')

    version('1.3.4', sha256='daa5de961aaaec7c1883c09db7748a7f221116a942d1397b35655db92ad4efb0')
    version('1.3.3', sha256='a7a39fe02a1dc514a9295c2bc44c15e311289f4aef140aa985abe17d5bd29016')
    version('1.3.2', sha256='8eb697a879245c6246ffabf2c1ed72a5ae335769f0772f55cbe4fee3e50223fe')
    version('1.3.1', sha256='d1c2f6bfd619c64594e5c7473acc9b8c373133a10412b69b26ccf35c80ca78e8')
    version('1.3.0', sha256='aad56b39a718abc65516485cc358e39348288fcd0b4f13ecb430486ab6d07630')
    version('1.2.0', sha256='e970759ceaea6172bdeabdec8cbdc7fd07b3e206f337b35635e52f2c5d182073')
    version('1.1.1', sha256='a92b9274c6091f6919b39358f14b44b70104d4e3480bce07601e941abcbd3106')
    version('1.1.0', sha256='9a3b923d78023b7a27710f2db4fb3318166b6054a12789906e707bd3467317f1')
    version('1.0.0', sha256='a7abb233ca2d8e681732db86f8902753f0395d45a54cfd63474fa3e7a1f650af')

    conflicts('platform=darwin', msg='libglvnd is linux specific')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')

    depends_on('libxext')
    depends_on('libx11')
    depends_on('glproto')

    @when('@master')
    def autoreconf(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()

    def configure_args(self):
        return [
            '--enable-egl',
            '--disable-gles',
            '--enable-glx'
        ]
