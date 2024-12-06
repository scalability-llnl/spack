# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUtils(PythonPackage):
    """Useful, oft-repeated things for Python"""

    homepage = "https://github.com/haaksmash/pyutils"
    url = "https://github.com/haaksmash/pyutils/archive/1.0.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("1.0.1", sha256="3a6552db1678e86a1b5e31107d20ae90dc5fb858ff7936b95367ee9d1b99e9ae")
    version("0.8.0", sha256="916672df4cf9647e44f0aa1b3b327eb361c3c0bac1b1e32a6cf723ca766a2d4b")

    depends_on("python@3.6:", type=("build", "run"), when="@1.0.0:")
    depends_on("py-setuptools", type="build")
