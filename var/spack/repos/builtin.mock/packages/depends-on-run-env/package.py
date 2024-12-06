# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DependsOnRunEnv(Package):
    """This package has a runtime dependency on another package which needs
    to perform shell modifications to run.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("modifies-run-env", type=("run",))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
