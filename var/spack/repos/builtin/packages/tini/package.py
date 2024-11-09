# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tini(CMakePackage):
    """A tiny but valid `init` for containers"""

    homepage = "https://github.com/krallin/tini"
    url = "https://github.com/krallin/tini/archive/refs/tags/v0.19.0.tar.gz"
    maintainers("teonnik", "Madeeks")

    license("MIT")

    version("0.19.0", sha256="0fd35a7030052acd9f58948d1d900fe1e432ee37103c5561554408bdac6bbf0d")

    depends_on("c", type="build")  # generated
    patch("tini_static_rpath_issue.patch", when="@0.19.0:")
