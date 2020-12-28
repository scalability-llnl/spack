# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gurobi(Package):
    """The Gurobi Optimizer was designed from the ground up to be the fastest,
    most powerful solver available for your LP, QP, QCP, and MIP (MILP, MIQP,
    and MIQCP) problems.

    Note: Gurobi is licensed software. You will need to create an account on
    the Gurobi homepage and download Gurobi Optimizer yourself. Spack will
    search your current directory for the download file. Alternatively, add
    this file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html

    Please set the path to licence file with the following command (for bash)
    export GRB_LICENSE_FILE=/path/to/gurobi/license/. See section 4 in
    $GUROBI_HOME/docs/quickstart_linux.pdf for more details."""

    homepage = "http://www.gurobi.com/index"
    manual_download = True

    version('7.5.2', '01f6dbb8d165838cca1664a1a14e4a85')

    # Licensing
    license_required = True
    license_vars     = ['GRB_LICENSE_FILE']
    license_url      = 'http://www.gurobi.com/downloads/download-center'

    def url_for_version(self, version):
        return "file://{0}/gurobi{1}_linux64.tar.gz".format(os.getcwd(), version)

    def setup_run_environment(self, env):
        env.set('GUROBI_HOME', self.prefix)

    def install(self, spec, prefix):
        install_tree('linux64', prefix)
