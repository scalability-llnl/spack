# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Qbank(Package):
    """QBank is a unique dynamic reservation-based allocation management system
    that manages the utilization of computational resources in a multi-project
    environment. It is used in conjunction with a resource management system
    allowing an organization to guarantee greater fairness and enforce mission
    priorities by associating a charge with the use of computational resources
    and allocating resource credits which limit how much of the resources may
    be used at what time and by whom. It tracks resource utilization and allows
    for insightful planning."""

    # QBank is so old that it no longer has (never had?) a homepage
    # but it was developed at Pacific Northwest National Laboratory
    # by Scott Jackson <Scott.Jackson@pnl.gov>
    homepage = "https://www.pnnl.gov/"
    url = "file://{0}/qbank-2.10.4.tar.gz".format(os.getcwd())
    manual_download = True

    version("2.10.4", md5="0820587353e63d32ddb49689dd4289e7")

    variant("doc", default=False, description="Build documentation")

    depends_on("openssl")

    depends_on("perl@5.6:5.16", type=("build", "run"))
    depends_on("perl-dbi@1.00:", type=("build", "run"))

    def configure_args(self):
        config_args = ["--prefix", self.prefix, "--logdir", self.prefix.var.log.qbank]

        return config_args

    def install(self, spec, prefix):
        perl = which("perl")
        perl("configure", *self.configure_args())
        make()

        if "+doc" in spec:
            make("docs")

        make("install")

        if "+doc" in spec:
            install_tree("doc", prefix.doc)

    def setup_run_environment(self, env):
        if "+doc" in self.spec:
            env.prepend_path("MANPATH", self.prefix.doc)
