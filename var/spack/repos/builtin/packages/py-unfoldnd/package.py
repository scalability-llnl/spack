# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUnfoldnd(PythonPackage):
    """N-dimensional unfold (im2col) and fold (col2im) in PyTorch."""

    homepage = "https://github.com/f-dangel/unfoldNd"
    pypi = "unfoldnd/unfoldnd-0.2.2.tar.gz"

    license("MIT")

    version("0.2.2", sha256="e8fdffeb68bc1b393ddc1b1c87056e0e4616db992e95c7dbc3dc90d564599397")

    with default_args(type="build"):
        depends_on("py-setuptools@38.3:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-torch")
        depends_on("py-numpy")
