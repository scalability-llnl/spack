# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdatrie(AutotoolsPackage):
    """datrie is an implementation of double-array structure for representing
    trie."""

    homepage = "https://linux.thai.net/projects/datrie"
    url = "https://github.com/tlwg/libdatrie/releases/download/v0.2.12/libdatrie-0.2.12.tar.xz"

    license("LGPL-2.1-or-later")

    version("0.2.12", sha256="452dcc4d3a96c01f80f7c291b42be11863cd1554ff78b93e110becce6e00b149")
    version("0.2.11", sha256="547c7bd2ab9e10ad65f3270cae8ca7027f52db9c30f7327d24354ad41a98e94b")

    depends_on("c", type="build")  # generated

    depends_on("doxygen@1.8.8:", type="build")
