# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Cpio(AutotoolsPackage, GNUMirrorPackage):
    """GNU cpio copies files into or out of a cpio or tar archive. The
       archive can be another file on the disk, a magnetic tape, or a pipe.
    """
    homepage = "https://www.gnu.org/software/cpio/"
    gnu_mirror_path = "cpio/cpio-2.13.tar.gz"

    executables = ['^cpio$']

    version('2.13', sha256='e87470d9c984317f658567c03bfefb6b0c829ff17dbf6b0de48d71a4c8f3db88')

    patch('https://src.fedoraproject.org/rpms/cpio/raw/dfe64c466d3ea2c8dfbd99700d9006f610064167/f/cpio-2.13-mutiple-definition.patch', sha256='d22633c368b8aedf4c08b23b6fbaa81a52404c8943ab04926404083ac10f1a4b', when='%gcc@10:')

    build_directory = 'spack-build'

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'\(GNU cpio\)\s+(\S+)', output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        spec = self.spec

        if name == 'cflags':
            if '%intel@:18.999' in spec:
                flags.append('-no-gcc')

            elif '%clang' in spec or '%fj' in spec:
                flags.append('--rtlib=compiler-rt')

        return (flags, None, None)
