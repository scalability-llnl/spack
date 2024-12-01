# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCallmonitor(PythonPackage):
    """A Simple Tool to Monitor and Log Function Calls"""

    homepage = "https://github.com/JBlaschke/call-monitor"
    pypi = "callmonitor/callmonitor-0.3.7.tar.gz"

    maintainers("DaxLynch")

    version("0.3.7", sha256="11bacfe5940c3f6aff223e8e761b033d540542b4d738f7fef38cd923b3be0cbc")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
