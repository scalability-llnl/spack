# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Transset(AutotoolsPackage, XorgPackage):
    """transset is an utility for setting opacity property."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/transset"
    xorg_mirror_path = "app/transset-1.0.1.tar.gz"

    license("MIT")

    version("1.0.3", sha256="adba0da81dacdebe5275ec0117dd08685e4f2f31afa0391f423e54906d0fb824")
    version("1.0.2", sha256="5c7d7d1bac36137f41ac3db84d7ed9b9fdac868608572bcba0bc1de40510ca67")
    version("1.0.1", sha256="87c560e69e05ae8a5bad17ff62ac31cda43a5065508205b109c756c0ab857d55")

    depends_on("c", type="build")

    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
