# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColored(PythonPackage):
    """Simple library for color and formatting to terminal

    Very simple Python library for color and formatting in terminal.
    Collection of color codes and names for 256 color terminal setups.
    The following is a list of 256 colors for Xterm, containing an example
    of the displayed color, Xterm Name, Xterm Number and HEX."""

    homepage = "https://gitlab.com/dslackw/colored"
    pypi     = "colored/colored-1.4.2.tar.gz"

    version('1.4.2', sha256='056fac09d9e39b34296e7618897ed1b8c274f98423770c2980d829fd670955ed')

    depends_on('py-setuptools', type='build')
