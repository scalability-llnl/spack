# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH11(PythonPackage):
    """A pure-Python, bring-your-own-I/O implementation of HTTP/1.1"""

    homepage = "https://github.com/python-hyper/h11"
    pypi = "h11/h11-0.10.0.tar.gz"

    license("MIT")

    version("0.13.0", sha256="70813c1135087a248a4d38cc0e1a0181ffab2188141a93eaf567940c3957ff06")
    version("0.12.0", sha256="47222cb6067e4a307d535814917cd98fd0a57b6788ce715755fa2b6c28b56042")
    version("0.11.0", sha256="3c6c61d69c6f13d41f1b80ab0322f1872702a3ba26e12aa864c928f6a43fbaab")
    version("0.10.0", sha256="311dc5478c2568cc07262e0381cdfc5b9c6ba19775905736c87e81ae6662b9fd")
    version("0.9.0", sha256="33d4bca7be0fa039f4e84d50ab00531047e53d6ee8ffbc83501ea602c169cae1")

    depends_on("py-setuptools", type="build")

    depends_on("python@3.6:", type=("build", "run"), when="@0.12.0:")
    depends_on("py-typing-extensions", type=("build", "run"), when="@0.13: ^python@:3.7")
