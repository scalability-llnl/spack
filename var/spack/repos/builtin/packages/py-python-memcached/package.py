# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonMemcached(PythonPackage):
    """This software is a 100% Python interface to the memcached memory cache
    daemon. It is the client side software which allows storing values in one
    or more, possibly remote, memcached servers. Search google for memcached
    for more information."""

    pypi = "python-memcached/python-memcached-1.59.tar.gz"

    version("1.59", sha256="a2e28637be13ee0bf1a8b6843e7490f9456fd3f2a4cb60471733c7b5d5557e4f")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.4.0:", type=("build", "run"))
