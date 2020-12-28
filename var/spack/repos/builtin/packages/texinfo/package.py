# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.package import *


class Texinfo(AutotoolsPackage, GNUMirrorPackage):
    """Texinfo is the official documentation format of the GNU project.

    It was invented by Richard Stallman and Bob Chassell many years ago,
    loosely based on Brian Reid's Scribe and other formatting languages
    of the time. It is used by many non-GNU projects as well."""

    homepage = "https://www.gnu.org/software/texinfo/"
    gnu_mirror_path = "texinfo/texinfo-6.0.tar.gz"

    executables = ['^info$']

    version('6.5', sha256='d34272e4042c46186ddcd66bd5d980c0ca14ff734444686ccf8131f6ec8b1427')
    version('6.3', sha256='300a6ba4958c2dd4a6d5ce60f0a335daf7e379f5374f276f6ba31a221f02f606')
    version('6.0', sha256='83d3183290f34e7f958d209d0b20022c6fe9e921eb6fe94c27d988827d4878d2')
    version('5.2', sha256='6b8ca30e9b6f093b54fe04439e5545e564c63698a806a48065c0bba16994cf74')
    version('5.1', sha256='50e8067f9758bb2bf175b69600082ac4a27c464cb4bcd48a578edd3127216600')
    version('5.0', sha256='2c579345a39a2a0bb4b8c28533f0b61356504a202da6a25d17d4d866af7f5803')

    depends_on('perl')

    # Fix unescaped braces in regexps.
    # Ref: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=898994
    patch('fix_unescaped_braces.patch', when='@6.3:')
    patch('fix_unescaped_braces_2.patch', when='@5.1:6.0')
    patch('fix_unescaped_braces_3.patch', when='@5.0')

    # Apply this fix to perform thread-safe processing in code
    # that uses the global locale.
    # Ref: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=902771
    patch('update_locale_handling.patch', when='@6.3:')

    patch('nvhpc.patch', when='%nvhpc')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'info \(GNU texinfo\)\s+(\S+)', output)
        return match.group(1) if match else None
