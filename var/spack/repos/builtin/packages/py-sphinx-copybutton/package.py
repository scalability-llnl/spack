# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxCopybutton(PythonPackage):
    """A small sphinx extension to add a "copy" button to code blocks."""

    homepage = "https://github.com/choldgraf/sphinx-copybutton"
    pypi = "sphinx-copybutton/sphinx-copybutton-0.2.12.tar.gz"

    license("MIT")

    version("0.2.12", sha256="9492883786984b6179c92c07ab0410237b26efa826adfa792acfd17b91a63e5c")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@1.8:")
