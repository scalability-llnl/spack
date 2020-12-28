# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libelf(AutotoolsPackage):
    """libelf lets you read, modify or create ELF object files in an
       architecture-independent way. The library takes care of size
       and endian issues, e.g. you can process a file for SPARC
       processors on an Intel-based system. Note: libelf is no longer
       maintained and packages that depend on libelf should migrate to
       elfutils."""

    # The original homepage no longer exists, but the tar file is
    # archived at fossies.org.
    # homepage = "http://www.mr511.de/software/english.html"

    homepage = "https://directory.fsf.org/wiki/Libelf"

    urls = [
        'https://fossies.org/linux/misc/old/libelf-0.8.13.tar.gz',
        'https://ftp.osuosl.org/pub/blfs/conglomeration/libelf/libelf-0.8.13.tar.gz'
    ]

    version('0.8.13', sha256='591a9b4ec81c1f2042a97aa60564e0cb79d041c52faa7416acb38bc95bd2c76d')

    provides('elf@0')

    def configure_args(self):
        args = ["--enable-shared",
                "--disable-dependency-tracking",
                "--disable-debug"]
        return args

    def install(self, spec, prefix):
        make('install', parallel=False)
