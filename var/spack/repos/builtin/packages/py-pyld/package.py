# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyld(PythonPackage):
    """This library is an implementation of the JSON-LD specification in
    Python.
    """

    homepage = "https://github.com/digitalbazaar/pyld"
    pypi = "PyLD/PyLD-2.0.3.tar.gz"

    license("BSD-3-Clause")

    version("2.0.3", sha256="287445f888c3a332ccbd20a14844c66c2fcbaeab3c99acd506a0788e2ebb2f82")

    depends_on("py-cachetools", type=("build", "run"))
    depends_on("py-frozendict", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
