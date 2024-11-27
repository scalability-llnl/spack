# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExtras(PythonPackage):
    """Useful extra bits for Python - things that shold be in the standard
    library."""

    homepage = "https://github.com/testing-cabal/extras"
    pypi = "extras/extras-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="132e36de10b9c91d5d4cc620160a476e0468a88f16c9431817a6729611a81b4e")

    depends_on("py-setuptools", type="build")
