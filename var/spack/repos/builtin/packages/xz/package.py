# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Xz(AutotoolsPackage, SourceforgePackage):
    """XZ Utils is free general-purpose data compression software with
    high compression ratio. XZ Utils were written for POSIX-like systems,
    but also work on some not-so-POSIX systems. XZ Utils are the successor
    to LZMA Utils."""

    homepage = "http://tukaani.org/xz/"
    sourceforge_mirror_path = "lzmautils/files/xz-5.2.5.tar.bz2"
    list_url = "http://tukaani.org/xz/old.html"

    executables = [r'^xz$']

    version('5.2.5', sha256='5117f930900b341493827d63aa910ff5e011e0b994197c3b71c08a20228a42df')
    version('5.2.4', sha256='3313fd2a95f43d88e44264e6b015e7d03053e681860b0d5d3f9baca79c57b7bf')
    version('5.2.3', sha256='fd9ca16de1052aac899ad3495ad20dfa906c27b4a5070102a2ec35ca3a4740c1')
    version('5.2.2', sha256='6ff5f57a4b9167155e35e6da8b529de69270efb2b4cf3fbabf41a4ee793840b5')
    version('5.2.0', sha256='f7357d7455a1670229b3cca021da71dd5d13b789db62743c20624bdffc9cc4a5')

    variant('pic', default=False,
            description='Compile with position independent code.')

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.cc_pic_flag)
        return (flags, None, None)

    @property
    def libs(self):
        return find_libraries(['liblzma'], root=self.prefix, recursive=True)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'xz \(XZ Utils\) (\S+)', output)
        return match.group(1) if match else None
