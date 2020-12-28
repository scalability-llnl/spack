# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBrew(RPackage):
    """brew implements a templating framework for mixing text and R code for
    report generation. brew template syntax is similar to PHP, Ruby's erb
    module, Java Server Pages, and Python's psp module."""

    homepage = "https://cloud.r-project.org/package=brew"
    url      = "https://cloud.r-project.org/src/contrib/brew_1.0-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/brew"

    version('1.0-6', sha256='d70d1a9a01cf4a923b4f11e4374ffd887ad3ff964f35c6f9dc0f29c8d657f0ed')
