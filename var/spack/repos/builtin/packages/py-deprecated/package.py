# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeprecated(PythonPackage):
    """Python @deprecated decorator to deprecate old python classes,
    functions or methods."""

    homepage = "https://github.com/tantale/deprecated"
    url = "https://github.com/tantale/deprecated/archive/v1.2.7.tar.gz"

    version("1.2.7", sha256="7db3c814ddcac9d79c5bae8a0e82a5bba55cb8e46f3d611d0d8611c34a72a783")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-wrapt@1.10:1.99999", type=("build", "run"))
    depends_on("py-setuptools", type="build")
