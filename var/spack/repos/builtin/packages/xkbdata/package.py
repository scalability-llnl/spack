# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xkbdata(AutotoolsPackage, XorgPackage):
    """The XKB data files for the various keyboard models, layouts,
    and locales."""

    homepage = "https://www.x.org/wiki/XKB/"
    xorg_mirror_path = "data/xkbdata-1.0.1.tar.gz"

    version("1.0.1", sha256="5b43ca5219cd4022a158a8d4bfa30308ea5e16c9b5270a64589ebfe7f875f430")

    depends_on("xkbcomp", type="build")
