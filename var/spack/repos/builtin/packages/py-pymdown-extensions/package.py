# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPymdownExtensions(PythonPackage):
    """Extensions for Python Markdown."""

    homepage = "https://github.com/facelessuser/pymdown-extensions"
    pypi = "pymdown_extensions/pymdown_extensions-9.5.tar.gz"

    license("MIT")

    version("9.5", sha256="3ef2d998c0d5fa7eb09291926d90d69391283561cf6306f85cd588a5eb5befa0")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-hatchling@0.21.1:", type="build")
    depends_on("py-markdown@3.2:", type=("build", "run"))
