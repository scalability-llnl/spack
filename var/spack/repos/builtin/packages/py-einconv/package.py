# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEinconv(PythonPackage):
    """Convolutions as tensor contractions (einsums) for PyTorch."""

    homepage = "https://github.com/f-dangel/einconv"
    pypi = "einconv/einconv-0.1.0.tar.gz"

    license("MIT")

    version("0.1.0", sha256="6b103881b1268e43d581f285da4fa72b073c95f31b92575133bafed9929b6d98")

    with default_args(type="build"):
        depends_on("py-setuptools@38.3:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-torch")
        depends_on("py-einops")
