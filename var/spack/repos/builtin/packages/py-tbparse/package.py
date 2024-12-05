# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTbparse(PythonPackage):
    """Load tensorboard event logs as pandas DataFrames."""

    homepage = "https://github.com/j3soon/tbparse"
    pypi = "tbparse/tbparse-0.0.7.tar.gz"

    license("Apache-2.0")

    version("0.0.7", sha256="0ddd3c764ceb1859bc0cb69ca355bff4fd5936c4bfe885e252e481564b2371a9")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-pandas@1.3:", type=("build", "run"))
    depends_on("py-tensorboard@2:", type=("build", "run"))
