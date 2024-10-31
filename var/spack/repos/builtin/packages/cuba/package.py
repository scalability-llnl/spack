# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cuba(AutotoolsPackage):
    """The Cuba library offers a choice of four independent routines for
    multidimensional numerical integration: Vegas, Suave, Divonne, and
    Cuhre."""

    homepage = "https://feynarts.de/cuba/"
    url = "https://feynarts.de/cuba/Cuba-4.2.2.tar.gz"

    maintainers("wdconinc")

    license("LGPL-3.0-only")

    version("4.2.2", sha256="8d9f532fd2b9561da2272c156ef7be5f3960953e4519c638759f1b52fe03ed52")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    parallel = False
