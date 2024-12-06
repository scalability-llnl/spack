# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPrwlock(PythonPackage):
    """Native process-shared rwlock support for Python"""

    homepage = "https://github.com/renatolfc/prwlock"
    pypi = "prwlock/prwlock-0.4.1.tar.gz"

    license("MIT")

    version("0.4.1", sha256="a2fa773cb877207ae5b54c7cf5d224b0215c9f7b9ef16a88d33eadc5c9e1466e")

    depends_on("py-setuptools", type="build")
