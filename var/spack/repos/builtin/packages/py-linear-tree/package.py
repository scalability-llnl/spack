# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinearTree(PythonPackage):
    """A python library to build Model Trees with Linear Models at the leaves."""

    homepage = "https://github.com/cerlymarco/linear-tree"
    pypi = "linear-tree/linear-tree-0.3.5.tar.gz"
    git = "https://github.com/cerlymarco/linear-tree.git"

    version("0.3.5", sha256="2db9fc976bcd693a66d8d92fdd7f97314125b3330eea4778885bfe62190d586c")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-learn@0.24.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
