# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Genfit(CMakePackage):
    """GenFit is an experiment-independent framework for track reconstruction in
    particle and nuclear physics"""

    homepage = "https://github.com/GenFit/GenFit"
    url = "https://github.com/GenFit/GenFit/archive/02-00-00.tar.gz"
    git = "https://github.com/GenFit/GenFit.git"

    maintainers("mirguest")

    tags = ["hep"]

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("02-00-05", sha256="8c37d1692e592f9f28a145c38aa41b0a6ed9211947846e9d10e34a2759ee446e")
    version("02-00-04", sha256="b833e40cfe5343424262d28f9cb715fc80255313a985508453ac17c3a522b273")
    version("02-00-03", sha256="23bb4c26740be96bd7933d30f3b683c6246b8f349116bc43d1c85117682e7a4b")
    version("02-00-02", sha256="b415abec7466d7fd15de6c37cd970c07a6581fe303fdfa3a8bc9258ea1c19d7d")
    version("02-00-01", sha256="e5a3eabf1ab53178fbd40aff0a8071bf48bac558ba1b798769106ccf230c4120")
    version("02-00-00", sha256="0bfd5dd152ad0573daa4153a731945824e0ce266f844988b6a8bebafb7f2dacc")
    # Untagged version from 2017-06-23 known to work with root@6.16.00
    version("b496504a", sha256="e1582b35782118ade08498adc03f3fda01979ff8bed61e0520edae46d7bfe477")

    depends_on("cxx", type="build")  # generated

    depends_on("root")
    depends_on("root@:6.16.00", when="@b496504a")
    depends_on("eigen")
    depends_on("googletest")

    # See https://github.com/GenFit/GenFit/pull/127
    conflicts("root@6.30:", when="@:02-00-04", msg="genfit cannot be built against root@6.30 ")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@:02-00-04"):
            # normally, as a cmake package root should be
            # automatically picked up after 'depends_on'
            # as it is added to CMAKE_PREFIX_PATH
            # but genfit cooks its own root cmake config
            # so this workaround is needed for now.
            root_prefix = self.spec["root"].prefix
            args.append("-DROOT_DIR=%s" % root_prefix)

        return args
