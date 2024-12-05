# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFqdn(PythonPackage):
    """Validates fully-qualified domain names against RFC 1123, so that they
    are acceptable to modern bowsers."""

    homepage = "https://github.com/ypcrts/fqdn"
    pypi = "fqdn/fqdn-1.5.1.tar.gz"

    license("MPL-2.0")

    version("1.5.1", sha256="105ed3677e767fb5ca086a0c1f4bb66ebc3c100be518f0e0d755d9eae164d89f")

    depends_on("py-setuptools", type="build")

    depends_on("py-cached-property@1.3:", when="^python@:3.7", type=("build", "run"))
