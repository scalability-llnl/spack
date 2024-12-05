# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNosexcover(PythonPackage):
    """A companion to the built-in nose.plugins.cover, this plugin will write
    out an XML coverage report to a file named coverage.xml."""

    homepage = "https://github.com/cmheisel/nose-xcover"
    pypi = "nosexcover/nosexcover-1.0.11.tar.gz"

    version("1.0.11", sha256="298c3c655da587f6cab8a666e9f4b150320032431062dea91353988d45c8b883")

    depends_on("py-setuptools", type="build")
    depends_on("py-nose", type=("build", "run"))
    depends_on("py-coverage@3.4:", type=("build", "run"))
