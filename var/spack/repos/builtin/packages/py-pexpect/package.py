# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPexpect(PythonPackage):
    """Pexpect allows easy control of interactive console applications."""

    homepage = "https://pexpect.readthedocs.io/en/stable/"
    pypi = "pexpect/pexpect-4.2.1.tar.gz"

    maintainers("TomMelt")

    license("ISC", checked_by="tommelt")

    version("4.9.0", sha256="ee7d41123f3c9911050ea2c2dac107568dc43b2d3b0c7557a33212c398ead30f")
    version("4.8.0", sha256="fc65a43959d153d0114afe13997d439c22823a27cefceb5ff35c2178c6784c0c")
    version("4.7.0", sha256="9e2c1fd0e6ee3a49b28f95d4b33bc389c89b20af6a1255906e90ff1262ce62eb")
    version("4.6.0", sha256="2a8e88259839571d1251d278476f3eec5db26deb73a70be5ed5dc5435e418aba")
    version("4.2.1", sha256="3d132465a75b57aa818341c6521392a06cc660feb3988d7f1074f39bd23c9a92")
    version("3.3", sha256="dfea618d43e83cfff21504f18f98019ba520f330e4142e5185ef7c73527de5ba")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-ptyprocess", type=("build", "run"))
    depends_on("py-ptyprocess@0.5:", type=("build", "run"), when="@4.7.0:")
