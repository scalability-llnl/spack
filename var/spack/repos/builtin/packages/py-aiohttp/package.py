# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAiohttp(PythonPackage):
    """Supports both client and server side of HTTP protocol.
    Supports both client and server Web-Sockets out-of-the-box and
    avoids Callbacks.  Provides Web-server with middlewares and
    plugable routing."""

    homepage = "https://github.com/aio-libs/aiohttp"
    pypi = "aiohttp/aiohttp-3.8.1.tar.gz"

    license("Apache-2.0")

    version("3.9.5", sha256="edea7d15772ceeb29db4aff55e482d4bcfb6ae160ce144f2682de02f6d693551")
    version("3.9.4", sha256="6ff71ede6d9a5a58cfb7b6fffc83ab5d4a63138276c771ac91ceaaddf5459644")
    version("3.9.0", sha256="09f23292d29135025e19e8ff4f0a68df078fe4ee013bca0105b2e803989de92d")
    version("3.8.4", sha256="bf2e1a9162c1e441bf805a1fd166e249d574ca04e03b34f97e2928769e91ab5c")
    version("3.8.1", sha256="fc5471e1a54de15ef71c1bc6ebe80d4dc681ea600e68bfd1cbce40427f0b7578")
    version("3.8.0", sha256="d3b19d8d183bcfd68b25beebab8dc3308282fe2ca3d6ea3cb4cd101b3c279f8d")
    version("3.7.4", sha256="5d84ecc73141d0a0d61ece0742bb7ff5751b0657dab8405f899d3ceb104cc7de")
    version("3.6.2", sha256="259ab809ff0727d0e834ac5e8a283dc5e3e0ecc30c4d80b3cd17a4139ce1f326")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:", when="@3.9:")
    depends_on("py-setuptools@46.4:", type="build")

    depends_on("py-attrs@17.3.0:", type=("build", "run"))
    depends_on("py-charset-normalizer@2:3", when="@3.8.4:", type=("build", "run"))
    depends_on("py-charset-normalizer@2", when="@3.8.0:3.8.3", type=("build", "run"))
    depends_on("py-multidict@4.5:6", when="@3.6.3:", type=("build", "run"))
    depends_on("py-multidict@4.5:4", when="@:3.6.2", type=("build", "run"))
    depends_on("py-async-timeout@4", when="@3.8.0 ^python@:3.10", type=("build", "run"))
    depends_on("py-async-timeout@3", when="@:3.7.4 ^python@:3.10", type=("build", "run"))
    depends_on("py-asynctest@0.13.0", when="@3.8.0: ^python@:3.7", type=("build", "run"))
    depends_on("py-yarl@1", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@3.8: ^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions@3.6.5:", when="@3.7", type=("build", "run"))
    depends_on("py-typing-extensions@3.6.5:", when="@:3.6 ^python@:3.7", type=("build", "run"))
    depends_on("py-frozenlist@1.1.1:", when="@3.8.1:", type=("build", "run"))
    depends_on("py-aiosignal@1.1.2:", when="@3.8.1:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-chardet@2.0:3", when="@:3.7", type=("build", "run"))
