# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libtree(CMakePackage):
    """ldd as a tree with an option to bundle dependencies into a
       single folder"""

    homepage = "https://github.com/haampie/libtree"
    url      = "https://github.com/haampie/libtree/releases/download/v1.0.3/sources.tar.gz"

    maintainers = ['haampie']

    version('1.2.1', sha256='26791c0f418b93d502879db0e1fd2fd3081b885ad87326611d992a5f8977a9b0')
    version('1.2.0', sha256='3e74655f22b1dcc19e8a1b9e7796b8ad44bc37f29e9a99134119e8521e28be97')
    version('1.1.4', sha256='38648f67c8fa72c3a4a3af2bb254b5fd6989c0f1362387ab298176db5cbbcc4e')
    version('1.1.3', sha256='4c681d7b67ef3d62f95450fb7eb84e33ff10a3b9db1f7e195b965b2c3c58226b')
    version('1.1.2', sha256='31641c6bf6c2980ffa7b4c57392460434f97ba66fe51fe6346867430b33a0374')
    version('1.1.1', sha256='3e8543145a40a94e9e2ce9fed003d2bf68294e1fce9607028a286bc132e17dc4')
    version('1.1.0', sha256='6cf36fb9a4c8c3af01855527d4931110732bb2d1c19be9334c689f1fd1c78536')
    version('1.0.4', sha256='b15a54b6f388b8bd8636e288fcb581029f1e65353660387b0096a554ad8e9e45')
    version('1.0.3', sha256='67ce886c191d50959a5727246cdb04af38872cd811c9ed4e3822f77a8f40b20b')
