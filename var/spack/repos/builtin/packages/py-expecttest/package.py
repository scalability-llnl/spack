# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExpecttest(PythonPackage):
    """This library implements expect tests (also known as "golden" tests)."""

    homepage = "https://github.com/ezyang/expecttest"
    pypi = "expecttest/expecttest-0.1.6.tar.gz"

    license("MIT")

    version("0.1.6", sha256="fd49563b6703b9c060a0bc946dfafc62bad74898867432192927eb1e5f9d8952")

    depends_on("python@:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
