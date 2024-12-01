# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeprecated(PythonPackage):
    """Python @deprecated decorator to deprecate old python classes,
    functions or methods."""

    homepage = "https://github.com/tantale/deprecated"
    pypi = "Deprecated/Deprecated-1.2.13.tar.gz"

    license("MIT")

    version("1.2.13", sha256="43ac5335da90c31c24ba028af536a91d41d53f9e6901ddb021bcc572ce44e38d")
    version("1.2.7", sha256="408038ab5fdeca67554e8f6742d1521cd3cd0ee0ff9d47f29318a4f4da31c308")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-wrapt@1.10:1", type=("build", "run"))
    depends_on("py-setuptools", type="build")
