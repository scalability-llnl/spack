# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCodespell(PythonPackage):
    """check code for common misspellings"""

    homepage = "https://github.com/codespell-project/codespell"
    pypi = "codespell/codespell-2.2.6.tar.gz"

    license("GPL-2.0", checked_by="cmelone")

    version("2.3.0", sha256="360c7d10f75e65f67bad720af7007e1060a5d395670ec11a7ed1fed9dd17471f")
    version("2.2.6", sha256="a8c65d8eb3faa03deabab6b3bbe798bea72e1799c7e9e955d57eca4096abcff9")

    depends_on("py-setuptools@64.0:", type="build")
    depends_on("py-setuptools-scm@6.2: +toml", type="build")
    conflicts("^py-setuptools-scm@8.0.0")
