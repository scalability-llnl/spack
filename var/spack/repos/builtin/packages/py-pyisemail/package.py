# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyisemail(PythonPackage):
    """pyIsEmail is a no-nonsense approach for checking whether that user-supplied
    email address could be real."""

    homepage = "https://github.com/michaelherold/pyIsEmail"
    pypi = "pyisemail/pyisemail-2.0.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("2.0.1", sha256="daf4b3fb2150a38f406b0aaba729e19fcd638a6d1c0549c25ff54c7b804618f8")

    depends_on("py-hatchling", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-dnspython@2.0.0:", type=("build", "run"))
