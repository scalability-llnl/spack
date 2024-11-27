# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLouie(PythonPackage):
    """Louie provides Python programmers with a straightforward way to
    dispatch signals between objects in a wide variety of contexts. It
    is based on PyDispatcher, which in turn was based on a highly-rated
    recipe in the Python Cookbook."""

    homepage = "https://github.com/11craft/louie/"
    url = "https://github.com/11craft/louie/archive/2.0.tar.gz"

    version("2.0", sha256="ac274ef672511357fc15d784df841c238ae13d00964094571eebabb0b14c54b2")
    version("1.1", sha256="4bc227171fc546d1a527ee3059fa17df6d35a0acc10db1f942dd3da42ad96408")

    depends_on("py-setuptools", type="build")
