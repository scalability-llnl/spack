# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FluxPython(PythonPackage):
    """Python bindings for the flux resource manager API"""

    homepage = "https://github.com/flux-framework/flux-python/"
    pypi = "flux-python/flux_python-0.70.0.tar.gz"

    license("LGPL-3.0-only")

    version("0.70.0", sha256="88835aaa4d8886a5db825f72940171b92a8d33abd4835915e97e1dbd1f09c49a")
    version("0.68.0", sha256="5ab31bffe0ea369e4cb204f809f7f4db63626f31e84e9cf9f83286d37bff96eb")
    version("0.66.0", sha256="56b6f0356e8bb143629332c1fb0ddaa16b7e6afdf1fa459bb9b3b35d1366c8e3")
    version("0.65.0", sha256="a3598835603fba21d09e76183bb1e8b939350118c57f1ca3d9f67994562eaded")
    version("0.63.0", sha256="963cd5e2198cd8c534c062a11815746469abe078ab23caa076fafada75d65cda")
    version("0.62.0", sha256="7121e02f81c87a8a0723019dad2c9800bbd749f3704ca54b9649e02ed89e87c3")
    version("0.61.2", sha256="a3cfe0125b97f39ecf34a1d7f479368f5152abc022be6adb44adb7356d099ba8")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))
