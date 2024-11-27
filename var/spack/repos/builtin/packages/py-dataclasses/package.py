# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataclasses(PythonPackage):
    """A backport of the dataclasses module for Python 3.6"""

    homepage = "https://github.com/ericvsmith/dataclasses"
    pypi = "dataclasses/dataclasses-0.7.tar.gz"

    version("0.8", sha256="8479067f342acf957dc82ec415d355ab5edb7e7646b90dc6e2fd1d96ad084c97")
    version("0.7", sha256="494a6dcae3b8bcf80848eea2ef64c0cc5cd307ffc263e17cdf42f3e5420808e6")

    depends_on("py-setuptools", type="build")

    # Python 3.6 is not supported for installation, but need to support bootstrapping,
    # so comment out the following line.
    # depends_on("python@3.6", type=("build", "run"))
    conflicts("^python@:3.5,3.7:")
