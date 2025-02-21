# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lbzip2(AutotoolsPackage):
    """Multi-threaded compression utility with support for bzip2
    compressed file format"""

    homepage = "https://lbzip2.org/"
    url = "http://archive.lbzip2.org/lbzip2-2.5.tar.gz"

    version("2.5", sha256="46c75ee93cc95eedc6005625442b2b8e59a2bef3ba80987d0491f055185650e9")
