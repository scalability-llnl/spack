# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstTransports(CMakePackage):
    """Provides transports like uGNI and verbs
       that run in the simulator"""

    homepage = "https://github.com/sstsimulator"
    git = "https://github.com/jjwilke/sst-transports.git"

    maintainers = ['jjwilke']

    version('master',  branch='master')

    depends_on("sst-macro")

    def cmake_args(self):
        args = []
        args.append("-DSSTMacro_ROOT=%s" % self.spec["sst-macro"].prefix)
        return args
