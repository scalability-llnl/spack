# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygtrie(PythonPackage):
    """A pure Python implementation of a trie data structure."""

    homepage = "https://github.com/mina86/pygtrie"
    pypi = "pygtrie/pygtrie-2.4.2.tar.gz"

    license("Apache-2.0")

    version("2.4.2", sha256="43205559d28863358dbbf25045029f58e2ab357317a59b11f11ade278ac64692")
    version("2.4.0", sha256="77700d2fcaab321ac65e86c2969fb4b64c116796baf52ab12d07de2e1f6cfc5d")
    version("2.3.2", sha256="6299cdedd2cbdfda0895c2dbc43efe8828e698c62b574f3ef7e14b3253f80e23")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
