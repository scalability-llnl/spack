# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbsd(AutotoolsPackage):
    """This library provides useful functions commonly found on BSD
    systems, and lacking on others like GNU systems, thus making it easier
    to port projects with strong BSD origins, without needing to embed the
    same code over and over again on each project.
    """

    homepage = "https://libbsd.freedesktop.org/wiki/"
    urls     = [
        "https://libbsd.freedesktop.org/releases/libbsd-0.9.1.tar.xz",
        "https://mirrors.dotsrc.org/pub/mirrors/exherbo/libbsd-0.9.1.tar.xz"
    ]

    version('0.11.3', sha256='ff95cf8184151dacae4247832f8d4ea8800fa127dbd15033ecfe839f285b42a1')
    version('0.11.2', sha256='9a7fbe60924d40ce4322a00b6f70be07b3704479b2bca1210dd1564924930ff5')
    version('0.11.1', sha256='0d018e78f85d7d724740a28408f0bf346b7bbe5dc1c7256fb21e640e2a3d5205')
    version('0.11.0', sha256='9043e24f5898eae6e0ce97bea4f2d15197e90f6e9b91d0c6a8d10fb1405fd562')
    version('0.10.0', sha256='34b8adc726883d0e85b3118fa13605e179a62b31ba51f676136ecb2d0bc1a887')
    version('0.9.1', sha256='56d835742327d69faccd16955a60b6dcf30684a8da518c4eca0ac713b9e0a7a4')
    version('0.9.0', sha256='8a469afd1bab340992cf99e1e6b7ae4f4c54882d663d8a2c5ea52250617afb01')
    version('0.8.7', sha256='f548f10e5af5a08b1e22889ce84315b1ebe41505b015c9596bad03fd13a12b31')
    version('0.8.6', sha256='467fbf9df1f49af11f7f686691057c8c0a7613ae5a870577bef9155de39f9687')

    patch('cdefs.h.patch', when='@0.8.6 %gcc@:4')
    patch('local-elf.h.patch', when='%intel')
    patch('nvhpc.patch', when='%nvhpc')

    # https://gitlab.freedesktop.org/libbsd/libbsd/issues/1
    conflicts('platform=darwin')

    depends_on('libmd', when='@0.11:')

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%pgi') or self.spec.satisfies('%nvhpc'):
            filter_file('-isystem', '-I', 'src/Makefile.in')
            # This is not a 1 for 1 replacement, requiring nvhpc.patch
            # to include config.h where needed
            filter_file('-include ', '-I ', 'src/Makefile.in')
            filter_file('-Wall -Wextra -Wno-unused-variable '
                        '-Wno-unused-parameter', '-Wall', 'configure')
