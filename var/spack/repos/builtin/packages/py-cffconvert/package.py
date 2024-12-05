# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCffconvert(PythonPackage):
    """Command line program to validate and convert CITATION.cff files."""

    homepage = "https://github.com/citation-file-format/cff-converter-python"
    pypi = "cffconvert/cffconvert-2.0.0.tar.gz"

    license("Apache-2.0")

    version("2.0.0", sha256="b4379ee415c6637dc9e3e7ba196605cb3cedcea24613e4ea242c607d9e98eb50")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-click@7.0:8", type=("build", "run"))
    depends_on("py-requests@2.20:2", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.16.0:", type=("build", "run"))
    depends_on("py-pykwalify@1.6:", type=("build", "run"))
    depends_on("py-jsonschema@3.0:3", type=("build", "run"))
