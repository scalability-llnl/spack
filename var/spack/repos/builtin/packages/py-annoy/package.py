# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnnoy(PythonPackage):
    """Annoy (Approximate Nearest Neighbors Oh Yeah) is a C++ library with Python
    bindings to search for points in space that are close to a given query point.
    It also creates large read-only file-based data structures that are mmapped into
    memory so that many processes may share the same data."""

    homepage = "https://github.com/spotify/annoy"
    pypi = "annoy/annoy-1.17.1.tar.gz"

    license("Apache-2.0")

    version("1.17.1", sha256="bf177dbeafb81f63b2ac1e1246b1f26a2acc82e73ba46638734d29d8258122da")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-nose@1:", type="build")
