# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConstantly(PythonPackage):
    """Symbolic constants in Python"""

    homepage = "https://github.com/twisted/constantly"
    pypi = "constantly/constantly-15.1.0.tar.gz"

    license("MIT")

    version("23.10.4", sha256="aa92b70a33e2ac0bb33cd745eb61776594dc48764b06c35e0efd050b7f1c7cbd")
    version("15.1.0", sha256="586372eb92059873e29eba4f9dec8381541b4d3834660707faf8ba59146dfc35")

    depends_on("py-setuptools", type="build")
    depends_on("py-versioneer+toml@0.29", type="build", when="@23.10.4:")
