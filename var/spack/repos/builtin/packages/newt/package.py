# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Newt(AutotoolsPackage):
    """A library for text mode user interfaces."""

    homepage = "https://pagure.io/newt"
    url = "https://pagure.io/releases/newt/newt-0.52.21.tar.gz"

    license("LGPL-2.0-only")

    version("0.52.21", sha256="265eb46b55d7eaeb887fca7a1d51fe115658882dfe148164b6c49fccac5abb31")
    version("0.52.20", sha256="8d66ba6beffc3f786d4ccfee9d2b43d93484680ef8db9397a4fb70b5adbb6dbc")
    version("0.52.19", sha256="08c0db56c21996af6a7cbab99491b774c6c09cef91cd9b03903c84634bff2e80")

    depends_on("c", type="build")  # generated

    depends_on("slang")
    depends_on("popt")
