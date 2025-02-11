# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUsagestats(PythonPackage):
    """Easily get usage statistics from the users of your program.

    Statistics will be collected but won’t be uploaded until the user opts in. A
    message will be printed on stderr asking the user to explicitly opt in or
    opt out.

    """

    homepage = "https://github.com/remram44/usagestats"

    pypi = "usagestats/usagestats-1.0.1.tar.gz"

    maintainers("charmoniumQ")

    version("1.0.1", sha256="d8887aa0f65769b1423b784e626ec6fb6ba6ed1432667e10d6115b783571be6d")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-distro", type=("build", "run"))
