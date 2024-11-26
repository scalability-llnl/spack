# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XorgDocs(AutotoolsPackage, XorgPackage):
    """This package provides miscellaneous documentation for the X Window
    System that doesn't better fit into other packages.

    The preferred documentation format for these documents is DocBook XML."""

    homepage = "https://gitlab.freedesktop.org/xorg/doc/xorg-docs"
    xorg_mirror_path = "doc/xorg-docs-1.7.1.tar.gz"

    maintainers("wdconinc")

    version("1.7.3", sha256="30f8fc4b435cda82f21d08d81c2e2fc9046ec7e20945e32ab7b63326674cf8c5")
    version("1.7.2", sha256="0c1e018868a00cb5a5bc8622ffd87e706e119ffa0949edde00d0d0d912663677")
    version("1.7.1", sha256="360707db2ba48f6deeb53d570deca9fa98218af48ead4a726a67f63e3ef63816")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros@1.8:", type="build")
    depends_on("util-macros@1.20:", type="build", when="@1.7.3:")
    depends_on("xorg-sgml-doctools@1.8:", type="build")
    depends_on("xmlto", type="build")
