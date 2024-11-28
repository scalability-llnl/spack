# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gurobi(Package):
    """The Gurobi Optimizer was designed from the ground up to be the fastest,
    most powerful solver available for your LP, QP, QCP, and MIP (MILP, MIQP,
    and MIQCP) problems."""

    # Note: Gurobi is licensed software. You will need to create an account on
    # the Gurobi homepage and download Gurobi Optimizer yourself. Spack will
    # search your current directory for the download file. Alternatively, add
    # this file to a mirror so that Spack can find it. For instructions on how
    # to set up a mirror, see
    # https://spack.readthedocs.io/en/latest/mirrors.html

    homepage = "https://www.gurobi.com"
    manual_download = True

    version("10.0.0", sha256="91a9ce1464f5f948809fcdfbdeb55f77698ed8a6d6cfa6985295424b6ece2bd4")
    version("9.5.2", sha256="95d8ca18b7f86116ba834a27fd6228c5b1708ae67927e7ea0e954c09374a2d0f")
    version("9.5.1", sha256="fa82859d33f08fb8aeb9da66b0fbd91718ed573c534f571aa52372c9deb891da")
    version("9.1.2", sha256="7f60bd675f79476bb2b32cd632aa1d470f8246f2b033b7652d8de86f6e7e429b")
    version("7.5.2", md5="01f6dbb8d165838cca1664a1a14e4a85")

    # Licensing
    license_required = True
    license_files = ["gurobi.lic"]
    license_vars = ["GRB_LICENSE_FILE"]
    license_url = "http://www.gurobi.com/downloads/download-center"

    extends("python")
    depends_on("python@2.7,3.6:")

    def url_for_version(self, version):
        return "file://{0}/gurobi{1}_linux64.tar.gz".format(os.getcwd(), version)

    def patch(self):
        # Strip out existing PYTHONPATH as the presence of that will generally
        # break given that Spack has likely set that for a different Python.
        gurobi_shell = join_path("linux64", "bin", "gurobi.sh")
        filter_file(r":\$PYTHONPATH", "", gurobi_shell)

    def setup_run_environment(self, env):
        env.set("GUROBI_HOME", self.prefix)
        env.set("GRB_LICENSE_FILE", join_path(self.prefix, "gurobi.lic"))

    def install(self, spec, prefix):
        install_tree("linux64", prefix)

    @run_after("install")
    def gurobipy(self):
        with working_dir("linux64"):
            python("setup.py", "install", "--prefix={0}".format(self.prefix))
