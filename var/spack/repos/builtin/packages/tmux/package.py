# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tmux(AutotoolsPackage):
    """Tmux is a terminal multiplexer.

    What is a terminal multiplexer? It lets you switch easily between several
    programs in one terminal, detach them (they keep running in the
    background) and reattach them to a different terminal. And do a lot more.
    """

    homepage = "http://tmux.github.io"
    url = "https://github.com/tmux/tmux/releases/download/2.6/tmux-2.6.tar.gz"

    version('3.1b', sha256='d93f351d50af05a75fe6681085670c786d9504a5da2608e481c47cf5e1486db9')
    version('3.0a', sha256='4ad1df28b4afa969e59c08061b45082fdc49ff512f30fc8e43217d7b0e5f8db9')
    version('2.9', sha256='34901232f486fd99f3a39e864575e658b5d49f43289ccc6ee57c365f2e2c2980')
    version('2.8', sha256='7f6bf335634fafecff878d78de389562ea7f73a7367f268b66d37ea13617a2ba')
    version('2.7', sha256='9ded7d100313f6bc5a87404a4048b3745d61f2332f99ec1400a7c4ed9485d452')
    version('2.6', sha256='b17cd170a94d7b58c0698752e1f4f263ab6dc47425230df7e53a6435cc7cd7e8')
    version('2.5', sha256='ae135ec37c1bf6b7750a84e3a35e93d91033a806943e034521c8af51b12d95df')
    version('2.4', sha256='757d6b13231d0d9dd48404968fc114ac09e005d475705ad0cd4b7166f799b349')
    version('2.3', sha256='55313e132f0f42de7e020bf6323a1939ee02ab79c48634aa07475db41573852b')
    version('2.2', sha256='bc28541b64f99929fe8e3ae7a02291263f3c97730781201824c0f05d7c8e19e4')
    version('2.1', sha256='31564e7bf4bcef2defb3cb34b9e596bd43a3937cad9e5438701a81a5a9af6176')
    version('1.9a', sha256='c5e3b22b901cf109b20dab54a4a651f0471abd1f79f6039d79b250d21c2733f5')

    # used by configure to e.g. find libtinfo
    depends_on('pkgconfig', type='build')
    depends_on('libevent')
    depends_on('ncurses')
