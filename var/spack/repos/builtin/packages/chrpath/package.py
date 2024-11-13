# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chrpath(AutotoolsPackage):
    """chrpath: Modifies the dynamic library load path (rpath and runpath)
    of compiled programs and libraries."""

    homepage = "https://directory.fsf.org/wiki/Chrpath"
    url = "https://cfhcable.dl.sourceforge.net/project/pisilinux/source/chrpath-0.16.tar.gz"

    license("GPL-2.0-or-later")

    version("0.16", sha256="bb0d4c54bac2990e1bdf8132f2c9477ae752859d523e141e72b3b11a12c26e7b")

    depends_on("c", type="build")  # generated
