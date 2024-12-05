# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyApeye(PythonPackage):
    """Handy tools for working with URLs and APIs."""

    homepage = "https://github.com/domdfcoding/apeye"
    pypi = "apeye/apeye-1.4.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("1.4.1", sha256="14ea542fad689e3bfdbda2189a354a4908e90aee4bf84c15ab75d68453d76a36")

    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-apeye-core@1:", type=("build", "run"))
    depends_on("py-domdf-python-tools@2.6:", type=("build", "run"))
    depends_on("py-platformdirs@2.3:", type=("build", "run"))
    depends_on("py-requests@2.24:", type=("build", "run"))
