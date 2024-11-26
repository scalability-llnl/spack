# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XapianCore(AutotoolsPackage):
    """Xapian is a highly adaptable toolkit which allows developers to easily
    add advanced indexing and search facilities to their own applications.
    It supports the Probabilistic Information Retrieval model and also
    supports a rich set of boolean query operators."""

    homepage = "https://xapian.org"
    url = "https://oligarchy.co.uk/xapian/1.4.19/xapian-core-1.4.19.tar.xz"

    license("GPL-2.0-or-later")

    version("1.4.19", sha256="1fca48fca6cc3526cc4ba93dd194fe9c1326857b78edcfb37e68d086d714a9c3")
    version("1.4.11", sha256="9f16b2f3e2351a24034d7636f73566ab74c3f0729e9e0492934e956b25c5bc07")
    version("1.4.3", sha256="7d5295511ca2de70463a29e75f6a2393df5dc1485bf33074b778c66e1721e475")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
