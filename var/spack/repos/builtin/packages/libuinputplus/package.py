# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libuinputplus(CMakePackage):
    """A c++ wrapper around libuinput."""

    homepage = "https://github.com/YukiWorkshop/libuInputPlus"
    url      = "https://github.com/YukiWorkshop/libuInputPlus/archive/v0.1.4.tar.gz"

    version('0.1.4', sha256='a537e156d11ad00c643b93cbd9b712d3ec9d0ae8e40731ff763fe9a6ffe97458')
