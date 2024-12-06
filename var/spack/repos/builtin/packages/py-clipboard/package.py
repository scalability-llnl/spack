# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClipboard(PythonPackage):
    """A cross platform clipboard operation library of Python."""

    homepage = "https://github.com/terryyin/clipboard"
    pypi = "clipboard/clipboard-0.0.4.tar.gz"

    license("MIT")

    version("0.0.4", sha256="a72a78e9c9bf68da1c3f29ee022417d13ec9e3824b511559fd2b702b1dd5b817")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyperclip@1.3:", type=("build", "run"))
