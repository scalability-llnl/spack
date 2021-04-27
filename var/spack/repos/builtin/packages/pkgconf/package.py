# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pkgconf(AutotoolsPackage):
    """pkgconf is a program which helps to configure compiler and linker
    flags for development frameworks. It is similar to pkg-config from
    freedesktop.org, providing additional functionality while also
    maintaining compatibility."""

    homepage = "http://pkgconf.org/"
    # URL must remain http:// so Spack can bootstrap curl
    url      = "http://distfiles.dereferenced.org/pkgconf/pkgconf-1.6.3.tar.xz"

    version('1.7.4',  sha256='d73f32c248a4591139a6b17777c80d4deab6b414ec2b3d21d0a24be348c476ab')
    version('1.7.3',  sha256='b846aea51cf696c3392a0ae58bef93e2e72f8e7073ca6ad1ed8b01c85871f9c0')
    version('1.6.3',  sha256='61f0b31b0d5ea0e862b454a80c170f57bad47879c0c42bd8de89200ff62ea210')
    version('1.6.1',  sha256='22b9ee38438901f9d60f180e5182821180854fa738fd071f593ea26a81da208c')
    version('1.6.0',  sha256='6135a3abb576672ba54a899860442ba185063f0f90dae5892f64f7bae8e1ece5')
    version('1.5.4',  sha256='9c5864a4e08428ef52f05a41c948529555458dec6d283b50f8b7d32463c54664')
    version('1.4.2',  sha256='bab39371d4ab972be1d539a8b10b6cc21f8eafc97f617102e667e82bd32eb234')
    version('1.4.0',  sha256='1d112ff35dad516ffbfbdb013df3a035140618fe7632ec44ffa894a9c713301b')
    version('1.3.10', sha256='62577d265fa9415a57a77a59dede5526b7ece3ef59a750434b281b262f0c1da9')
    version('1.3.8',  sha256='fc06f058e6905435481f649865ca51000192c91808f307b1053ca5e859cb1488')

    provides('pkgconfig')

    # https://github.com/spack/spack/issues/11704
    patch('nvhpc.patch', when='@1.7.3%nvhpc')

    # TODO: Add a package for the kyua testing framework
    # depends_on('kyua', type='test')

    # https://github.com/spack/spack/issues/3525
    conflicts('%pgi')

    tags = ['build-tools']

    executables = ['^pkgconf$', '^pkg-config$']

    @classmethod
    def determine_version(cls, exe):
        exe = Executable(exe)

        # Make sure this is actually pkgconf, not pkg-config
        if 'usage: pkgconf' not in exe('--help', output=str, error=str):
            return None

        version = exe('--version', output=str, error=str).rstrip()

        return version

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        env.append_path('ACLOCAL_PATH', self.prefix.share.aclocal)

    @run_after('install')
    def link_pkg_config(self):
        symlink('pkgconf', '{0}/pkg-config'.format(self.prefix.bin))
        symlink('pkgconf.1',
                '{0}/pkg-config.1'.format(self.prefix.share.man.man1))
