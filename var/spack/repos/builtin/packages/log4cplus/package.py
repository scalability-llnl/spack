# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Log4cplus(CMakePackage):
    """log4cplus is a simple to use C++ logging API
    providing thread-safe, flexible, and arbitrarily
    granular control over log management and configuration."""

    homepage = "https://sourceforge.net/projects/log4cplus/"
    url = "https://download.sourceforge.net/project/log4cplus/log4cplus-stable/2.0.1/log4cplus-2.0.1.tar.bz2"

    license("Apache-2.0 AND BSD-2-Clause")

    version("2.0.7", sha256="8fadbafee2ba4e558a0f78842613c9fb239c775d83f23340d091084c0e1b12ab")
    version("2.0.1", sha256="43baa7dec3db1ecc97dd9ecf3b50220439d2c7041d15860c36aa1d48dcf480b5")
    version("1.2.1", sha256="ada80be050033d7636beb894eb54de5575ceca95a5572e9437b0fc4ed7d877c4")

    depends_on("cxx", type="build")  # generated
