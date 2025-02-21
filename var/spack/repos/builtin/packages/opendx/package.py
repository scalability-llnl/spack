# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Opendx(AutotoolsPackage):
    """Open Visualization Data Explorer."""

    homepage = "https://github.com/Mwoolsey/OpenDX"
    git = "https://github.com/Mwoolsey/OpenDX.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("motif")  # lesstif also works, but exhibits odd behaviors
    depends_on("gl")

    @run_before("autoreconf")
    def distclean(self):
        make("distclean")
