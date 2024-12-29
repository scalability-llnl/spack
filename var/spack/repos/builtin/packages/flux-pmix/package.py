# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class FluxPmix(AutotoolsPackage):
    """A flux shell plugin to bootstrap openmpi v5+"""

    homepage = "https://github.com/flux-framework/flux-pmix"
    url = "https://github.com/flux-framework/flux-pmix/releases/download/v0.1.0/flux-pmix-0.1.0.tar.gz"
    git = "https://github.com/flux-framework/flux-pmix.git"

    maintainers("grondo")

    version("main", branch="main")
    version("0.5.0", sha256="f382800b1a342df0268146ea7ce33011299bf0c69a46ac8a52e87de6026c9322")
    version("0.4.0", sha256="f7f58891fc9d9a97a0399b3ab186f2cae30a75806ba0b4d4c1307f07b3f6d1bc")
    version("0.3.0", sha256="88edb2afaeb6058b56ff915105a36972acc0d83204cff7f4a4d2f65a5dee9d34")
    version("0.2.0", sha256="d09f1fe6ffe54f83be4677e1e727640521d8110090515d94013eba0f58216934")

    depends_on("c", type="build")  # generated

    depends_on("flux-core@0.49:", when="@0.3:")
    depends_on("flux-core@0.30.0:")
    depends_on("pmix@v4.1.0:")
    depends_on("openmpi")

    depends_on("pkgconfig", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def autoreconf(self, spec, prefix):
        if not os.path.exists("configure"):
            # Bootstrap with autotools
            bash = which("bash")
            bash("./autogen.sh")

    @run_after("install")
    def add_pluginpath(self):
        spec = self.spec
        pluginpath = join_path(self.prefix.lib, "flux/shell/plugins/pmix.so")
        if spec.satisfies("@:0.3.0"):
            rcfile = join_path(self.prefix.etc, "flux/shell/lua.d/mpi/openmpi@5.lua")
            filter_file(r"pmix/pmix.so", pluginpath)
        else:
            rcdir = join_path(self.prefix.etc, "flux/shell/lua.d")
            rcfile = join_path(rcdir, "pmix.lua")
            mkdirp(rcdir)
            with open(rcfile, "w") as fp:
                fp.write('plugin.load("' + pluginpath + '")')

    def setup_run_environment(self, env):
        spec = self.spec
        env.prepend_path("FLUX_SHELL_RC_PATH", join_path(self.prefix.etc, "flux/shell/lua.d"))
        if spec.satisfies("@0.3.0:"):
            env.prepend_path(
                "FLUX_PMI_CLIENT_SEARCHPATH", join_path(self.prefix.lib, "flux/upmi/plugins")
            )
