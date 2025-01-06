# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNvitop(PythonPackage):
    """
    An interactive NVIDIA-GPU process viewer and beyond,
    the one-stop solution for GPU process management.
    """

    homepage = "https://nvitop.readthedocs.io/"
    pypi = "nvitop/nvitop-1.4.0.tar.gz"

    license("Apache-2.0")

    version("1.4.0", sha256="92f313e9bd89fe1a9d54054e92f490f34331f1b7847a89ddaffd6a7fde1437bb")

    depends_on("py-nvidia-ml-py")
    depends_on("py-psutil")
    depends_on("py-cachetools")
    depends_on("py-termcolor")
    depends_on("py-setuptools")
