# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bump2version(PythonPackage):
    """This is a maintained fork of the excellent bumpversion project."""

    homepage = "https://github.com/c4urself/bump2version"
    pypi = "bump2version/bump2version-1.0.1.tar.gz"

    depends_on("py-setuptools", type="build")

    license("MIT")

    version("1.0.1", sha256="762cb2bfad61f4ec8e2bdf452c7c267416f8c70dd9ecb1653fd0bbb01fa936e6")
