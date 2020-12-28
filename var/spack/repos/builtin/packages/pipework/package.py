# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pipework(Package):
    """
    Pipework lets you connect together containers in arbitrarily complex
    scenarios.
    """

    homepage = "https://github.com/jpetazzo/pipework"
    git      = "https://github.com/jpetazzo/pipework.git"

    version('master', branch='master')

    def install(self, spec, prefix):
        install_tree('.', prefix)
