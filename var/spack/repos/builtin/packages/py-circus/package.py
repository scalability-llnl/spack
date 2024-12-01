# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCircus(PythonPackage):
    """Circus is a program that will let you run and watch
    multiple processes and sockets.
    """

    homepage = "https://github.com/circus-tent/circus"
    pypi = "circus/circus-0.18.0.tar.gz"

    license("Apache-2.0")

    version("0.18.0", sha256="193ce8224e068ced66724cf483106fb6674b51a57583ac1a0e7ed7a7ee8c71ab")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.4:3", type="build")

    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pyzmq@17.0:", type=("build", "run"))
    depends_on("py-tornado@5.0.2:", type=("build", "run"))
