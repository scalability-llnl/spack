# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class IntelPin(Package):
    """Intel Pin is a dynamic binary instrumentation framework for the IA-32,
    x86-64 and MIC instruction-set architectures that enables the creation of
    dynamic program analysis tools."""

    homepage = "http://www.pintool.org"
    maintainers = ['matthiasdiener']

    version('3.15', sha256='51ab5a381ff477335050b20943133965c5c515d074ad6afb801a898dae8af642', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.15-98253-gb56e429b1-gcc-linux.tar.gz')
    version('3.14', sha256='6c3b477c88673e0285fcd866a37a4fa47537d461a8bf48416ae3e9667eb7529b', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.14-98223-gb010a12c6-gcc-linux.tar.gz')
    version('3.13', sha256='04a36e91f3f85119c3496f364a8806c82bb675f7536a8ab45344c9890b5e2714', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.13-98189-g60a6ef199-gcc-linux.tar.gz')
    version('3.11', sha256='aa5abca475a6e106a75e6ed4ba518fb75a57549a59f00681e6bd6e3f221bd23a', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.11-97998-g7ecce2dac-gcc-linux.tar.gz')
    version('3.10', sha256='7c8f14c3a0654bab662b58aba460403138fa44517bd40052501e8e0075b2702a', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.10-97971-gc5e41af74-gcc-linux.tar.gz')
    version('3.7',  sha256='4730328795be61f1addb0e505a3792a4b4ca80b1b9405acf217beec6b5b90fb8', url='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.7-97619-g0d0c92f4f-gcc-linux.tar.gz')
    version('2.14', sha256="1c29f589515772411a699a82fc4a3156cad95863a29741dfa6522865d4d281a1", url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz")

    def install(self, spec, prefix):
        install_tree('.', prefix)
        mkdir(prefix.bin)
        symlink(join_path(prefix, 'pin'), join_path(prefix.bin, 'pin'))
