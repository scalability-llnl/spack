# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Byteman(MavenPackage):
    """Byteman is a tool which makes it easy to trace, monitor and test
    the behaviour of Java application and JDK runtime code."""

    homepage = "https://www.jboss.org/byteman"
    url = "https://github.com/bytemanproject/byteman/archive/4.0.12.tar.gz"

    license("BSD-3-Clause")

    version("4.0.12", sha256="72fdc904d7b8df9e743fbb5ae84e51ffc81d32b6e0b0b80fc7ac165dd8c9c7c2")
    version("4.0.11", sha256="8e4af6019702c8b22f354962f35f197f9ba2c8699235aac77ebd9263ac12261b")
    version("4.0.10", sha256="1b3c9e66fc3f230e407904db1ac43eb5cd4c33620f0d0f9f6c0cb23e4d28784e")
    version("4.0.9", sha256="4ffffa9e0bbc45d5c47d443dcae21191531e8b68ade9423d109d40826bf0bd2b")
    version("4.0.8", sha256="f357d759c1dad52f4ae626d07fb2cf7c62855b7421723633d90ac49d83bd154b")
    version("4.0.7", sha256="542d688c804cd7baa7efad59a94ef8e5d21cc81f3e897f31152c96a7df896aa5")
