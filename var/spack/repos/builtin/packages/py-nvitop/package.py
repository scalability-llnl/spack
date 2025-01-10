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

    maintainers("nboelte")

    license("Apache-2.0", checked_by="nboelte")

    version("1.4.0", sha256="92f313e9bd89fe1a9d54054e92f490f34331f1b7847a89ddaffd6a7fde1437bb")

    depends_on("py-nvidia-ml-py@11.450.51:12.561", type=("build", "run"))
    depends_on("py-psutil@5.6.6:", type=("build", "run"))
    depends_on("py-cachetools@1.0.1:", type=("build", "run"))
    depends_on("py-termcolor@1.0.0:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # Windows support would require the package py-windows-curses to be available in spack.
    # depends_on("py-colorama@0.4:", when="platform=windows", type=("build", "run"))
    # depends_on("py-windows-curses@2.2.0:", when="platform=windows", type=("build", "run"))
    conflicts("platform=windows")
