# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCocaPytorch(PythonPackage):
    """CoCa, Contrastive Captioners are Image-Text Foundation Models -
    Pytorch"""

    homepage = "https://github.com/lucidrains/CoCa-pytorch"
    pypi = "CoCa-pytorch/CoCa-pytorch-0.1.0.tar.gz"

    license("MIT", checked_by="alex391")

    version("0.1.0", sha256="119c83812d140ad197cf4e992db8c373d908af0bffd0a87015546b6a1cf0a316")

    depends_on("py-setuptools", type="build")
    depends_on("py-einops@0.4:", type=("build", "run"))
    depends_on("py-torch@1.6:", type=("build", "run"))
