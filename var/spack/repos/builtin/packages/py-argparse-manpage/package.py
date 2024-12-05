# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgparseManpage(PythonPackage):
    """Build manual page from python's ArgumentParser object."""

    homepage = "https://github.com/praiskup/argparse-manpage"
    pypi = "argparse-manpage/argparse-manpage-4.5.tar.gz"

    license("Apache-2.0")

    version("4.5", sha256="213c061878a10bf0e40f6a293382f6e82409e5110d0683b16ebf87f903d604db")

    variant("setuptools", default=False, description="Enable the setuptools.builds_meta backend")

    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type="build")

    depends_on("py-tomli", when="^python@:3.10", type=("build", "run"))

    depends_on("py-setuptools", when="+setuptools", type=("build", "run"))
