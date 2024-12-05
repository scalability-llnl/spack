# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSocketio(PythonPackage):
    """Python implementation of the Socket.IO realtime server."""

    homepage = "https://github.com/miguelgrinberg/python-socketio"
    pypi = "python-socketio/python-socketio-1.8.4.tar.gz"

    version("1.8.4", sha256="13807ce17e85371d15b31295a43b1fac1c0dba1eb5fc233353a3efd53aa122cc")

    variant(
        "eventlet",
        default=True,
        description="Pulls in optional eventlet dependency, required"
        " for using the zmq implementation.",
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.9.0:", type=("build", "run"))
    depends_on("py-python-engineio@1.2.1:", type=("build", "run"))
    depends_on("py-eventlet", when="+eventlet", type=("build", "run"))
