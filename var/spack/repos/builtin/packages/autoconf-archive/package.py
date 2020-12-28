# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class AutoconfArchive(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Autoconf Archive is a collection of more than 500 macros for
    GNU Autoconf."""

    homepage = "https://www.gnu.org/software/autoconf-archive/"
    gnu_mirror_path = "autoconf-archive/autoconf-archive-2019.01.06.tar.xz"

    version('2019.01.06', sha256='17195c833098da79de5778ee90948f4c5d90ed1a0cf8391b4ab348e2ec511e3f')
