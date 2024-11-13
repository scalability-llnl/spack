# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfastcommon(Package):
    """
    Libfastcommon is a c common functions library extracted from my open
    source project FastDFS. this library is very simple and stable.
    functions including: string, logger, chain, hash, socket, ini file
    reader, base64 encode / decode, url encode / decode, fast timer,
    skiplist, object pool etc. detail info please see the c header files.
    """

    homepage = "https://github.com/happyfish100/libfastcommon"
    url = "https://github.com/happyfish100/libfastcommon/archive/V1.0.43.tar.gz"

    version("1.0.43", sha256="05425aed8e6bc7ba283abba4e1bb500cc7f8c873c35bb86712d7123144a37b4c")
    version("1.0.42", sha256="653c781b8e19a53f69aa8b1d823a832270e310438385f4c176a337304c03bc52")
    version("1.0.41", sha256="23cc5900bdf82fe907084deaf4e36a4f1857ac2a7378a2999a6c806bd3b22562")
    version("1.0.40", sha256="ebb89a1bfeb5b140f596fd3e2a0ff202420be05a4d80ef67ddcfdbb248b9fef8")
    version("1.0.39", sha256="72ca36f83f3453564ca09d2d0c31354b868cf52ef5a24cfb15e66d0e505c90ac")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        sh = which("sh")
        sh("make.sh")
        sh("make.sh", "install")
        install_tree(".", prefix)
