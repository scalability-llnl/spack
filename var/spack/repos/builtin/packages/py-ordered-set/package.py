# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOrderedSet(PythonPackage):
    """An OrderedSet is a mutable data structure that is a hybrid of a list and
    a set. It remembers the order of its entries, and every entry has an index
    number that can be looked up."""

    homepage = "https://github.com/LuminosoInsight/ordered-set"
    pypi = "ordered-set/ordered-set-4.0.2.tar.gz"

    license("MIT")

    version("4.1.0", sha256="694a8e44c87657c59292ede72891eb91d34131f6531463aab3009191c77364a8")
    version("4.0.2", sha256="ba93b2df055bca202116ec44b9bead3df33ea63a7d5827ff8e16738b97f33a95")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@4.1:")
    depends_on("py-setuptools", type="build", when="@:4.0")
    depends_on("py-flit-core@3.2:3", type="build", when="@4.1:")
