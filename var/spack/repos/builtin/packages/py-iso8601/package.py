# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIso8601(PythonPackage):
    """Simple module to parse ISO 8601 dates"""

    homepage = "https://github.com/micktwomey/pyiso8601"
    pypi = "iso8601/iso8601-0.1.14.tar.gz"

    license("MIT")

    version("1.1.0", sha256="32811e7b81deee2063ea6d2e94f8819a86d1f3811e49d23623a41fa832bef03f")
    version("1.0.2", sha256="27f503220e6845d9db954fb212b95b0362d8b7e6c1b2326a87061c3de93594b1")
    version("0.1.14", sha256="8aafd56fa0290496c5edbb13c311f78fa3a241f0853540da09d9363eae3ebd79")

    depends_on("python@3.6.2:3", when="@1:", type=("build", "run"))
    depends_on("py-poetry-core@1:", when="@1:", type="build")

    depends_on("py-setuptools", when="@:0", type="build")
