# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aespipe(AutotoolsPackage):
    """aespipe program is AES encrypting or decrypting pipe. It reads from
    standard input and writes to standard output."""

    homepage = "https//loop-aes.sourceforge.net/"
    url = "https://sourceforge.net/projects/loop-aes/files/aespipe/v2.4f/aespipe-v2.4f.tar.bz2"

    license("Intel")

    version("2.4f", sha256="b135e1659f58dc9be5e3c88923cd03d2a936096ab8cd7f2b3af4cb7a844cef96")
    version("2.4e", sha256="bad5abb8678c2a6062d22b893171623e0c8e6163b5c1e6e5086e2140e606b93a")
    version("2.4d", sha256="c5ce656e0ade49b93e1163ec7b35450721d5743d8d804ad3a9e39add0389e50f")
    version("2.4c", sha256="260190beea911190a839e711f610ec3454a9b13985d35479775b7e26ad4c845e")
    version("2.4b", sha256="4f08611966998f66266f03d40d0597f94096164393c8f303b2dfd565e9d9b59d")
    version("2.3e", sha256="4e63a5709fdd0bffdb555582f9fd7a0bd1842e429420159accaf7f60c5d3c70f")
    version("2.3d", sha256="70330cd0710446c9ddf8148a7713fd73f1dc5e0b13fc4d3c75590305b2e3f008")

    depends_on("c", type="build")  # generated
