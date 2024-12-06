# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMergedeep(PythonPackage):
    """A deep merge function for Python."""

    homepage = "https://github.com/clarketm/mergedeep"
    pypi = "mergedeep/mergedeep-1.3.4.tar.gz"

    license("MIT")

    version("1.3.4", sha256="0096d52e9dad9939c3d975a774666af186eda617e6ca84df4c94dec30004f2a8")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
