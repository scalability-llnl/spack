# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLagom(PythonPackage):
    """Lagom is a dependency injection container
    designed to give you 'just enough' help with building your dependencies.
    """

    homepage = "https://lagom-di.readthedocs.io"
    url = "https://github.com/meadsteve/lagom/archive/refs/tags/2.2.0.tar.gz"
    git = "https://github.com/meadsteve/lagom.git"

    license("MIT")

    version("2.2.0", sha256="69f701a2f81d9ca0ea7c93a5b15f7420bbe03d14175ec128959ad82e2b67460b")

    depends_on("py-setuptools@59.6:", type="build")
    depends_on("py-mypy@0.971", type="build")
