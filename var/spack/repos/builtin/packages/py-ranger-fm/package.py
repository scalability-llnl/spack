# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRangerFm(PythonPackage):
    """A VIM-inspired filemanager for the console"""

    pypi = "ranger-fm/ranger-fm-1.9.2.tar.gz"
    git = "https://github.com/ranger/ranger.git"

    version("1.9.2", sha256="0ec62031185ad1f40b9faebd5a2d517c8597019c2eee919e3f1c60ce466d8625")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
