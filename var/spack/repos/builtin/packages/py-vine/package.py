# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVine(PythonPackage):
    """Promises, promises, promises."""

    pypi = "vine/vine-1.2.0.tar.gz"

    license("CC-BY-SA-4.0")

    version("5.0.0", sha256="7d3b1624a953da82ef63462013bbd271d3eb75751489f9807598e8f340bd637e")
    version("1.3.0", sha256="133ee6d7a9016f177ddeaf191c1f58421a1dcc6ee9a42c58b34bed40e1d2cd87")
    version("1.2.0", sha256="ee4813e915d0e1a54e5c1963fde0855337f82655678540a6bc5996bca4165f76")

    depends_on("py-setuptools", type="build")
