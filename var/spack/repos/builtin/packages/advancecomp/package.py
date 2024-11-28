# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Advancecomp(AutotoolsPackage):
    """AdvanceCOMP contains recompression utilities for your .zip archives,
    .png images, .mng video clips and .gz files."""

    homepage = "https://www.advancemame.it"
    url = "https://github.com/amadvance/advancecomp/archive/v2.1.tar.gz"

    license("GPL-3.0-or-later")

    version("2.6", sha256="799397b10d087d0147d6af117a5a473120f1369f0a3a3d68bf953abc0b749b75")
    version("2.5", sha256="b6b4333453f028565896dd3547bc930f062df82832d7992cc130ca951c2890a1")
    version("2.1", sha256="6113c2b6272334af710ba486e8312faa3cee5bd6dc8ca422d00437725e2b602a")
    version("2.0", sha256="caa63332cd141db17988eb89c662cf76bdde72f60d4de7cb0fe8c7e51eb40eb7")
    version("1.23", sha256="fe89d6ab382efc6b6be536b8d58113f36b83d82783d5215c261c14374cba800a")
    version("1.22", sha256="b8c482027a5f78d9a7f871cbba19cc896ed61653d1d93034c9dbe55484952605")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("zlib-api", type="link")
