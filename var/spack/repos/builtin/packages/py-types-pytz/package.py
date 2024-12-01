# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesPytz(PythonPackage):
    """This is a PEP 561 type stub package for the pytz package. It can be used
    by type-checking tools like mypy, pyright, pytype, PyCharm, etc. to check
    code that uses pytz."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-pytz/types-pytz-2023.3.0.0.tar.gz"

    version(
        "2023.3.0.0", sha256="ecdc70d543aaf3616a7e48631543a884f74205f284cefd6649ddf44c6a820aac"
    )

    depends_on("py-setuptools", type="build")
