# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColored(PythonPackage):
    """Simple library for color and formatting to terminal

    Very simple Python library for color and formatting in terminal.
    Collection of color codes and names for 256 color terminal setups.
    The following is a list of 256 colors for Xterm, containing an example
    of the displayed color, Xterm Name, Xterm Number and HEX."""

    homepage = "https://gitlab.com/dslackw/colored"
    pypi = "colored/colored-1.4.2.tar.gz"

    version("2.2.4", sha256="595e1dd7f3b472ea5f12af21d2fec8a2ea2cf8f9d93e67180197330b26df9b61")
    version("1.4.2", sha256="056fac09d9e39b34296e7618897ed1b8c274f98423770c2980d829fd670955ed")

    depends_on("py-setuptools", type="build", when="@1.4.2")
    depends_on("py-flit-core@3.2.0:3", type="build", when="@2.2.4:")
