# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPep8Naming(PythonPackage):
    """Check PEP-8 naming conventions, plugin for flake8."""

    homepage = "https://github.com/PyCQA/pep8-naming"
    pypi = "pep8-naming/pep8-naming-0.10.0.tar.gz"

    license("MIT")

    version("0.10.0", sha256="f3b4a5f9dd72b991bf7d8e2a341d2e1aa3a884a769b5aaac4f56825c1763bf3a")
    version("0.7.0", sha256="624258e0dd06ef32a9daf3c36cc925ff7314da7233209c5b01f7e5cdd3c34826")

    depends_on("py-setuptools", type="build")
    depends_on("py-flake8-polyfill@1.0.2:1", type=("build", "run"))
