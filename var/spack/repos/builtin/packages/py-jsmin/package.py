# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJsmin(PythonPackage):
    """JavaScript minifier."""

    homepage = "https://github.com/tikitu/jsmin/"
    pypi = "jsmin/jsmin-2.2.2.tar.gz"

    license("MIT")

    version("3.0.1", sha256="c0959a121ef94542e807a674142606f7e90214a2b3d1eb17300244bbb5cc2bfc")
    version("2.2.2", sha256="b6df99b2cd1c75d9d342e4335b535789b8da9107ec748212706ef7bbe5c2553b")

    depends_on("py-setuptools", type="build")
    # They use use_2to3, so must be setuptools<58
    # https://github.com/tikitu/jsmin/blob/release-2.2.2/setup.py#L10
    depends_on("py-setuptools@:57", type="build", when="@:2")
