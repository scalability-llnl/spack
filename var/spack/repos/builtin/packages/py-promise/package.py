# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPromise(PythonPackage):
    """This is a implementation of Promises in Python. It is a super set of
    Promises/A+ designed to have readable, performant code and to provide
    just the extensions that are absolutely necessary for
    using promises in Python."""

    homepage = "https://github.com/syrusakbary/promise"
    pypi = "promise/promise-2.3.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("2.3", sha256="dfd18337c523ba4b6a58801c164c1904a9d4d1b1747c7d5dbf45b693a49d93d0")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
