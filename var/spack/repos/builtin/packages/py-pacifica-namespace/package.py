# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPacificaNamespace(PythonPackage):
    """Python Pacifica Namespace Library"""

    homepage = "https://github.com/pacifica/pacifica-namespace/"
    pypi = "pacifica-namespace/pacifica-namespace-0.0.2.tar.gz"

    license("LGPL-3.0-only")

    version("0.0.2", sha256="a8f59aea1203a1557f7f57887b61e92f8450c74a8522798c5ddecf8fffb0b224")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
