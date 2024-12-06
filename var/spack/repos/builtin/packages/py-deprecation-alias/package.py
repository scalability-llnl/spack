# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDeprecationAlias(PythonPackage):
    """Wrapper providing support for deprecated aliases."""

    homepage = "https://github.com/domdfcoding/deprecation-alias"
    pypi = "deprecation_alias/deprecation-alias-0.3.2.tar.gz"

    license("Apache-2.0")

    version("0.3.2", sha256="1c9e1a5ddd0a276a1a18e7a4f9d56b53232217491c4549eaa45e51753013ce76")

    depends_on("py-wheel@0.34.2:", type="build")
    depends_on("py-setuptools@40.6:", type="build")
    conflicts("^py-setuptools@61")
    depends_on("py-deprecation@2.1:", type=("build", "run"))
    depends_on("py-packaging@20.4:", type=("build", "run"))
