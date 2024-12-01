# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlake8ImportOrder(PythonPackage):
    """Flake8 and pylama plugin that checks the ordering of import statements."""

    homepage = "https://github.com/PyCQA/flake8-import-order"
    pypi = "flake8-import-order/flake8-import-order-0.18.1.tar.gz"

    license("LGPL-3.0-only")

    version("0.18.1", sha256="a28dc39545ea4606c1ac3c24e9d05c849c6e5444a50fb7e9cdd430fc94de6e92")

    depends_on("py-pycodestyle", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
