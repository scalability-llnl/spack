# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRply(PythonPackage):
    """A pure Python Lex/Yacc that works with RPython."""

    homepage = "https://github.com/alex/rply/"
    pypi = "rply/rply-0.7.8.tar.gz"

    license("BSD-3-Clause")

    version("0.7.8", sha256="2a808ac25a4580a9991fc304d64434e299a8fc75760574492f242cbb5bb301c9")

    depends_on("py-setuptools", type="build")
    depends_on("py-appdirs", type=("build", "run"))
