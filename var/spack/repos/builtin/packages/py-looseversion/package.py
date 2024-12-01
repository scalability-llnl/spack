# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLooseversion(PythonPackage):
    """Version numbering for anarchists and software realists."""

    homepage = "https://github.com/effigies/looseversion"
    pypi = "looseversion/looseversion-1.0.2.tar.gz"

    version("1.2.0", sha256="c64e71c0b29030683b4ea75aee431db2d25c4e6e533590e52129f1d9e51de204")
    version("1.0.2", sha256="8b9f2e649eb81620c4527ba33ba87505eb69d4bb3f66523b34182a0450c294bc")

    depends_on("py-hatchling", when="@1.1.1:", type="build")
    depends_on("py-setuptools@40.8:", when="@:1.0.2", type="build")
