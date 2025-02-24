# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEmaPytorch(PythonPackage):
    """Easy way to keep track of exponential moving average version of your
    pytorch module"""

    homepage = "https://github.com/lucidrains/ema-pytorch"
    pypi = "ema_pytorch/ema_pytorch-0.5.1.tar.gz"

    license("MIT", checked_by="alex391")

    version("0.7.3", sha256="de640f1d1a054c79607aebfcfd4b8dfff1fba1110bf0c8f7d37517637450938a")
    version("0.5.1", sha256="e825212a44e8faae5d2cf2a1349961c4416cba0496ffa64d37718d8b06f206b2")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@2:", when="@0.7:", type=("build", "run"))
    depends_on("py-torch@1.6:", type=("build", "run"))
