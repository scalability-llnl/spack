# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bbcp(Package):
    """Securely and quickly copy data from source to target"""

    homepage = "https://www.slac.stanford.edu/~abh/bbcp/"
    git = "https://www.slac.stanford.edu/~abh/bbcp/bbcp.git"

    maintainers("vanderwb")

    # Stanford's git server does not support "smart https" shallow clones
    version("master", branch="master", get_full_repo=True)

    depends_on("zlib-api")
    depends_on("openssl")
    depends_on("libnsl")

    def install(self, spec, prefix):
        cd("src")
        make()
        # BBCP wants to build the executable in a directory whose name depends
        # on the system type
        makesname = Executable("../MakeSname")
        bbcp_executable_path = "../bin/%s/bbcp" % makesname(output=str).rstrip("\n")
        destination_path = "%s/bin/" % prefix
        mkdirp(destination_path)
        install(bbcp_executable_path, destination_path)
