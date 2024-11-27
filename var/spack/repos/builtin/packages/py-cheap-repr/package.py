# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyCheapRepr(PythonPackage):
    """This library provides short, fast, configurable string representations,
    and an easy API for registering your own. It's an improvement of the
    standard library module reprlib (repr in Python 2)."""

    pypi = "cheap-repr/cheap_repr-0.5.1.tar.gz"

    license("MIT", checked_by="jmlapre")

    version("0.5.1", sha256="31ec63b9d8394aa23d746c8376c8307f75f9fca0b983566b8bcf13cc661fe6dd")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm+toml", type="build")
