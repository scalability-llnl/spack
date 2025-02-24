# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pipework(Package):
    """
    Pipework lets you connect together containers in arbitrarily complex
    scenarios.
    """

    homepage = "https://github.com/jpetazzo/pipework"
    git = "https://github.com/jpetazzo/pipework.git"

    license("Apache-2.0")

    version("master", branch="master")

    def install(self, spec, prefix):
        install_tree(".", prefix)
