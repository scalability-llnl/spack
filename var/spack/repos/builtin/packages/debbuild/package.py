# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Debbuild(AutotoolsPackage):
    """Build deb packages from rpm specifications."""

    homepage = "https://github.com/debbuild/debbuild"
    url = "https://github.com/debbuild/debbuild/archive/20.04.0.tar.gz"

    license("GPL-2.0-or-later")

    version("20.04.0", sha256="e17c4f5b37e8c16592ebd99281884cabc053fb890af26531e9825417047d1430")

    depends_on("gettext")
