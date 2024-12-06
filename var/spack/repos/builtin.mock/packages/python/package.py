# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Python(Package):
    """Dummy Python package to demonstrate preferred versions."""

    homepage = "http://www.python.org"
    url = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz"

    extendable = True

    version("3.8.0", md5="d41d8cd98f00b204e9800998ecf8427e")
    version("3.7.1", md5="aaabbbcccdddeeefffaaabbbcccddd12")
    version("3.5.1", md5="be78e48cdfc1a7ad90efff146dce6cfe")
    version("3.5.0", md5="a56c0c0b45d75a0ec9c6dee933c41c36")
    version("2.7.11", md5="6b6076ec9e93f05dd63e47eb9c15728b", preferred=True)
    version("2.7.10", md5="d7547558fd673bd9d38e2108c6b42521")
    version("2.7.9", md5="5eebcaa0030dc4061156d3429657fb83")
    version("2.7.8", md5="d4bca0159acb0b44a781292b5231936f")
