# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKaggle(PythonPackage):
    """Official API for https://www.kaggle.com, accessible using a command line
    tool implemented in Python. Beta release - Kaggle reserves the right to
    modify the API functionality currently offered."""

    homepage = "https://github.com/Kaggle/kaggle-api"
    pypi = "kaggle/kaggle-1.5.12.tar.gz"

    license("Apache-2.0")

    version("1.5.12", sha256="b4d87d107bff743aaa805c2b382c3661c4c175cdb159656d4972be2a9cef42cb")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.10:", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-python-slugify", type=("build", "run"))
    depends_on("py-urllib3", type=("build", "run"))
