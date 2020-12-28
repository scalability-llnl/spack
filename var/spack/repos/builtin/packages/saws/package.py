# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Saws(AutotoolsPackage):
    """The Scientific Application Web server (SAWs) turns any C or C++
       scientific or engineering application code into a webserver,
       allowing one to examine (and even modify) the state of the
       simulation with any browser from anywhere."""

    homepage = "https://bitbucket.org/saws/saws/wiki/Home"
    git      = "https://bitbucket.org/saws/saws.git"

    version('develop', tag='master')
    version('0.1.1', tag='v0.1.1')
    version('0.1.0', tag='v0.1.0')

    depends_on('python', type='build')
