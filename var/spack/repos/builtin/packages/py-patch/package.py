# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPatch(PythonPackage):
    """Library to parse and apply unified diffs."""

    homepage = "https://github.com/techtonik/python-patch"
    pypi = "patch/patch-1.16.zip"

    version("1.16", sha256="c62073f356cff054c8ac24496f1a3d7cfa137835c31e9af39a9f5292fd75bd9f")

    depends_on("py-setuptools", type="build")
