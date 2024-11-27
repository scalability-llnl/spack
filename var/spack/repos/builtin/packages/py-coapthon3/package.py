# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCoapthon3(PythonPackage):
    """CoAPthon3 is a porting to python3 of my CoAPthon library.
    CoAPthon3 is a python3 library to the CoAP protocol compliant
    with the RFC. Branch is available for the Twisted framework."""

    homepage = "https://github.com/Tanganelli/CoAPthon3/"
    url = "https://github.com/Tanganelli/CoAPthon3/archive/1.0.1.tar.gz"

    license("MIT")

    version("1.0.1", sha256="331150a581708d47b208cee3b067ced80a00f0cc1278e913ec546e6c6b28bffd")
    version("1.0", sha256="63eb083269c2a286aedd206d3df17ab67fa978dc43caf34eaab9498da15c497a")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx", type=("build", "run"))
    depends_on("py-cachetools", type=("build", "run"))
