# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dnstracer(MakefilePackage):
    """Dnstracer determines where a given Domain Name Server gets
    its information from, and follows the chain of DNS servers back to
    the servers which know the data.
    """

    homepage = "https://github.com/Orc/dnstracer"
    git = "https://github.com/Orc/dnstracer.git"

    license("BSD-2-Clause")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        configure = Executable("./configure.sh")
        configure("--prefix={0}".format(prefix))
