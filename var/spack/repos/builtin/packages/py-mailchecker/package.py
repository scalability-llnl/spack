# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMailchecker(PythonPackage):
    """Cross-language email validation. Backed by a database of thousands
    throwable email providers"""

    homepage = "https://github.com/FGRibreau/mailchecker"
    pypi = "mailchecker/mailchecker-4.0.3.tar.gz"

    license("MIT")

    version("4.0.3", sha256="00dbe9739c754366233eb3887c5deef987672482a26e814314c3e749fc7b1d1f")

    depends_on("py-setuptools", type="build")
