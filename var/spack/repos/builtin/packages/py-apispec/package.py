# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyApispec(PythonPackage):
    """A pluggable API specification generator."""

    homepage = "https://github.com/marshmallow-code/apispec"
    pypi = "apispec/apispec-6.0.2.tar.gz"

    license("MIT")

    version("6.0.2", sha256="e76d80b739edef4be213092a6384ad7fd933ba7d64f6d5a0aff8d4da1bef7887")
    version("4.7.1", sha256="79029486d36a0d7f3c659dbf6ae50a91fbed0c22dcd5376f592e076c130bc7f9")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-packaging@21.3:", type=("build", "run"))
