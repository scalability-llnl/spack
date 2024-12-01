# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pciutils(MakefilePackage):
    """This package contains the PCI Utilities."""

    homepage = "https://mj.ucw.cz/sw/pciutils/"
    url = "https://github.com/pciutils/pciutils/archive/v3.7.0.tar.gz"

    license("GPL-2.0-only")

    version("3.7.0", sha256="ea768aa0187ba349391c6c157445ecc2b42e7d671fc1ce8c53ff5ef513f1e2ab")
    version("3.6.4", sha256="551d0ac33f030868b7e95c29e58dc2b1882455dbc9c15c15adf7086e664131f1")
    version("3.6.3", sha256="7ab0fbb35cffa326eb852539260562bac14f3d27cda8c70bc2cf3211ed97c014")

    depends_on("c", type="build")  # generated

    variant("lib", default=False, description="Install libraries with headers")

    def build(self, spec, prefix):
        make("PREFIX={0}".format(prefix))

    def install(self, spec, prefix):
        if "+lib" in spec:
            make("install-lib", "install", "PREFIX={0}".format(prefix))
        else:
            make("install", "PREFIX={0}".format(prefix))

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
