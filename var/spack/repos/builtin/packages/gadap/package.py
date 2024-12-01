# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gadap(AutotoolsPackage):
    """Enables OPeNDAP access of in situ data."""

    homepage = "http://cola.gmu.edu/grads/gadoc/supplibs.html"
    url = "http://cola.gmu.edu/grads/Supplibs/2.1/src/gadap-2.0.tar.gz"

    maintainers("vanderwb")

    license("GPL-2.0-only")

    version("2.0", sha256="ae9a989ca00ec29fb40616383d170883f07c022456db338399982a8a94ec0100")

    depends_on("cxx", type="build")  # generated

    depends_on("curl@7.18.0:")
    depends_on("libdap4")
    depends_on("libxml2")

    # libdap uses namespacing in recent versions, so we need to patch this source
    patch("cxx-updates.patch")

    def setup_build_environment(self, env):
        env.set("CFLAGS", "-fPIC")
        env.set("CXXFLAGS", "-fPIC")
