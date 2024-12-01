# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypeshedClient(PythonPackage):
    """A library for accessing stubs in typeshed."""

    homepage = "https://github.com/JelleZijlstra/typeshed_client"
    pypi = "typeshed-client/typeshed_client-2.1.0.tar.gz"

    license("MIT")

    version("2.1.0", sha256="da1969ec48c342197ddec655c873100ece38fd93e6827a1e6377793a16526f28")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-importlib-resources@1.4:", type=("build", "run"))
