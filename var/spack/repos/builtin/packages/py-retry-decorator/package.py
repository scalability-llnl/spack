# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRetryDecorator(PythonPackage):
    """Decorator for retrying when exceptions occur"""

    homepage = "https://github.com/pnpnpn/retry-decorator"
    pypi = "retry-decorator/retry_decorator-1.1.1.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("1.1.1", sha256="e1e8ad02e518fe11073f2ea7d80b6b8be19daa27a60a1838aff7c731ddcf2ebe")

    depends_on("py-setuptools", type="build")
