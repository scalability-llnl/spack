# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCerberus(PythonPackage):
    """Lightweight, extensible schema and data validation
    tool for Python dictionaries"""

    homepage = "http://docs.python-cerberus.org/"
    pypi = "Cerberus/Cerberus-1.3.4.tar.gz"

    license("0BSD")

    version("1.3.4", sha256="d1b21b3954b2498d9a79edf16b3170a3ac1021df88d197dc2ce5928ba519237c")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
