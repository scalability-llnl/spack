# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mbdyn(AutotoolsPackage):
    """MBDyn is the first and possibly the only free general purpose
    multibody dynamics analysis software."""

    homepage = "https://www.mbdyn.org/"
    url = "https://www.mbdyn.org/userfiles/downloads/mbdyn-1.7.3.tar.gz"

    license("GPL-2.0-or-later")

    version("1.7.3", sha256="3cf05cd1cb14c1af3d987aac119b6ecf0d835bc1aee06bc4cf7cc5a245c1f36d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Failed to build mbdyn with gcc@4.8.5 and gcc@9.2.0
    conflicts("%gcc@:5.0,9.0:")
