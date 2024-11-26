# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXpyb(AutotoolsPackage):
    """xpyb provides a Python binding to the X Window System protocol
    via libxcb."""

    homepage = "https://xcb.freedesktop.org/"
    url = "https://xcb.freedesktop.org/dist/xpyb-1.3.1.tar.gz"

    version("1.3.1", sha256="4056d11f94f17ed4342563955682193c7d004e80e5fa689816f87f3795549c17")

    depends_on("c", type="build")  # generated

    extends("python")

    depends_on("libxcb@1.5:")

    depends_on("xcb-proto@1.7.1:")
