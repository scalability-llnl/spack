# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQiskitIbmProvider(PythonPackage):
    """Qiskit IBM Quantum Provider for accessing the quantum devices and simulators
    at IBM"""

    homepage = "https://github.com/Qiskit/qiskit-ibm-provider"
    pypi = "qiskit-ibm-provider/qiskit-ibm-provider-0.5.1.tar.gz"

    license("Apache-2.0")

    version("0.5.1", sha256="0135d455d5fc4238efe1b852767c243fb995f003fbcac0bb836608426a0c0597")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-qiskit-terra@0.23.1:", type=("build", "run"))
    depends_on("py-requests@2.19:", type=("build", "run"))
    depends_on("py-requests-ntlm@1.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.13:", type=("build", "run"))
    depends_on("py-urllib3@1.21.1:", type=("build", "run"))
    depends_on("py-python-dateutil@2.8.0:", type=("build", "run"))
    depends_on("py-websocket-client@1.5.1:", type=("build", "run"))
    depends_on("py-websockets@10.0:", type=("build", "run"))
    depends_on("py-typing-extensions@4.3:", type=("build", "run"))
