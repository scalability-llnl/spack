# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskSocketio(PythonPackage):
    """Flask-SocketIO gives Flask applications access to low latency
    bi-directional communications between the clients and the server.
    The client-side application can use any of the SocketIO official clients
    libraries in Javascript, C++, Java and Swift, or any compatible client to
    establish a permanent connection to the server.
    """

    homepage = "https://flask-socketio.readthedocs.io"
    pypi = "Flask-SocketIO/Flask-SocketIO-2.9.6.tar.gz"

    version("2.9.6", sha256="f49edfd3a44458fbb9f7a04a57069ffc0c37f000495194f943a25d370436bb69")

    depends_on("py-setuptools", type="build")
    depends_on("py-flask@0.9:", type=("build", "run"))
    depends_on("py-python-socketio@1.6.1:", type=("build", "run"))
    depends_on("py-werkzeug", type=("build", "run"))
