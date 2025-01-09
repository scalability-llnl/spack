# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonMagic(PythonPackage):
    """A python wrapper for libmagic.

    This project is named python-magic but imports as the module name "magic".
    """

    homepage = "https://github.com/ahupp/python-magic"
    pypi = "python-magic/python-magic-0.4.15.tar.gz"

    license("MIT")

    version("0.4.27", sha256="c1ba14b08e4a5f5c31a302b7721239695b2f0f058d125bd5ce1ee36b9d9d3c3b")
    version("0.4.24", sha256="de800df9fb50f8ec5974761054a708af6e4246b03b4bdaee993f948947b0ebcf")
    version("0.4.15", sha256="f3765c0f582d2dfc72c15f3b5a82aecfae9498bd29ca840d72f37d7bd38bfcd5")

    depends_on("python@2.7.0:2.7,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("file", type="run")
