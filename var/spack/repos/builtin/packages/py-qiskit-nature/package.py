# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQiskitNature(PythonPackage):
    """Qiskit Nature is an open-source framework which supports
    solving quantum mechanical natural science problems using
    quantum computing algorithms"""

    homepage = "https://github.com/Qiskit/qiskit-nature"
    pypi = "qiskit-nature/qiskit-nature-0.2.2.tar.gz"

    license("Apache-2.0")

    version("0.2.2", sha256="ce3558d4acf2511111cc398361146af36391d67e5a9fe9c4bd0f727cb56022bf")

    depends_on("fortran", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@40.1.0:", type="build")

    depends_on("py-qiskit-terra@0.18.0:", type=("build", "run"))
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-scipy@1.4:", type=("build", "run"))
    depends_on("py-psutil@5:", type=("build", "run"))
    depends_on("py-h5py@:3.2", type=("build", "run"))
    depends_on("py-scikit-learn@0.20.0:", type=("build", "run"))
