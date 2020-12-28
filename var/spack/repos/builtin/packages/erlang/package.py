# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Erlang(AutotoolsPackage):
    """
    Erlang is a programming language and runtime system for building
    massively scalable soft real-time systems with requirements on
    high availability.
    """

    homepage = "https://erlang.org/"
    url      = "https://erlang.org/download/otp_src_22.2.tar.gz"

    version('23.0', sha256='42dcf3c721f4de59fe74ae7b65950c2174c46dc8d1dd4e27c0594d86f606a635')
    version('22.2', sha256='89c2480cdac566065577c82704a48e10f89cf2e6ca5ab99e1cf80027784c678f')
    version('22.1', sha256='cd33a102cbac6dd1c7b1e7a9a0d82d13587771fac4e96e8fff92e403d15e32c8')
    version('22.0', sha256='042e168d74055a501c75911694758a30597446accd8c82ec569552b9e9fcd272')
    version('21.3', sha256='69a743c4f23b2243e06170b1937558122142e47c8ebe652be143199bfafad6e4')
    version('21.2', sha256='f6b07bf8e6705915679a63363ce80faaa6b7c231e7236cde443d6445f7430334')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')
    depends_on('ncurses', type='link')
