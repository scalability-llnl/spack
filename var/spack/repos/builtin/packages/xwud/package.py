# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xwud(AutotoolsPackage, XorgPackage):
    """xwud allows X users to display in a window an image saved in a
    specially formatted dump file, such as produced by xwd."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xwud"
    xorg_mirror_path = "app/xwud-1.0.4.tar.gz"

    version("1.0.6", sha256="262171b0c434966ddbbe8a54afb9615567ad74d4cc2e823e14e51e099ec3ab0d")
    version("1.0.5", sha256="24d51e236ec3d1dd57c73679136029a14808aee5a2edda152d61598ba018c697")
    version("1.0.4", sha256="b7c124ccd87f529daedb7ef01c670ce6049fe141fd9ba7f444361de34510cd6c")

    depends_on("c", type="build")

    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
