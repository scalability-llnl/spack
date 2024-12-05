# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCssutils(PythonPackage):
    """A CSS Cascading Style Sheets library for Python."""

    homepage = "https://github.com/jaraco/cssutils"
    pypi = "cssutils/cssutils-2.7.1.tar.gz"

    maintainers("LydDeb")

    license("LGPL-3.0-or-later")

    version("2.7.1", sha256="340ecfd9835d21df8f98500f0dfcea0aee41cb4e19ecbc2cf94f0a6d36d7cb6c")

    depends_on("py-setuptools@56:", type="build")
    depends_on("py-setuptools-scm@3.4.1:+toml", type="build")
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
