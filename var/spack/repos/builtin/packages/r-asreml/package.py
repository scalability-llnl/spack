# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class RAsreml(RPackage):
    """ASReml-R is a statistical package that fits linear mixed models using
    Residual Maximum Likelihood (REML) in the R environment."""

    homepage = "https://vsni.co.uk/software/asreml-r"

    manual_download = True
    license_required = True
    license_vars = ["vsni_LICENSE"]
    license_files = ["vsni.lic"]

    maintainers("snehring")

    license("UNKNOWN", checked_by="snehring")

    version(
        "4.2.0.302_R42", sha256="93196b68a987fd0a8d26fa7463cab60bd35c7be750c4832332945d71907425cd"
    )
    version(
        "4.2.0.302_R43", sha256="0a685521c80e3263ebb852886d3e1bd31213bd83507e7fffca34261ae18523f9"
    )

    depends_on("r@4.2.0:4.2", type=("build", "run"), when="@4.2.0.302_R42")
    depends_on("r@4.3.0:4.3", type=("build", "run"), when="@4.2.0.302_R43")
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))

    def url_for_version(self, version):
        return f"file://{os.getcwd()}//asreml_{version}_x86_64-pc-linux-gnu.tar.gz"

    def setup_run_environment(self, env):
        env.set("vsni_LICENSE", join_path(self.prefix, "vsni.lic"))
