# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWebsockets(PythonPackage):
    """websockets is a library for building WebSocket servers and
    clients in Python with a focus on correctness and simplicity."""

    homepage = "https://github.com/aaugustin/websockets"
    pypi = "websockets/websockets-10.4.tar.gz"

    license("BSD-3-Clause")

    version("10.4", sha256="eef610b23933c54d5d921c92578ae5f89813438fded840c2e9809d378dc765d3")
    version("10.3", sha256="fc06cc8073c8e87072138ba1e431300e2d408f054b27047d047b549455066ff4")
    version("10.1", sha256="181d2b25de5a437b36aefedaf006ecb6fa3aa1328ec0236cdde15f32f9d3ff6d")
    version("8.1", sha256="5c65d2da8c6bce0fca2528f69f44b2f977e06954c8512a952222cea50dad430f")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
