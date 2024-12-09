# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDogpileCache(PythonPackage):
    """dogpile.cache is a Python caching API which provides a generic
    interface to caching backends of any variety."""

    homepage = "https://dogpilecache.sqlalchemy.org/en/latest/"
    pypi = "dogpile.cache/dogpile.cache-1.3.3.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("1.3.3", sha256="f84b8ed0b0fb297d151055447fa8dcaf7bae566d4dbdefecdcc1f37662ab588b")

    depends_on("py-setuptools@61.2:", type="build")
    depends_on("py-decorator@4.0.0:", type=("build", "run"))
    depends_on("py-stevedore@3.0.0:", type=("build", "run"))
    depends_on("py-typing-extensions@4.0.1:", type=("build", "run"), when="^python@:3.10")
