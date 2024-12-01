# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from datetime import datetime

from spack.package import *


class Stata(Package):
    """STATA is a general-purpose statistical software package developed
    by StataCorp."""

    # Known limitations of this installer:
    # * This really only installs the command line version of the program. To
    #   install GUI support there are extra packages needed that I can't easily
    #   test right now (should be installable via yum as a temp workaround):
    #   libgtk-x11-2.0.so libgdk-x11-2.0.so libatk-1.0.so libgdk_pixbuf-2.0.so
    #   Those libraries appear to be provided by: pango gdk-pixbuf2 gtk2
    #
    # * There are two popular environment variables that can be set, but vary from
    #   place to place, so future enhancement maybe to support STATATMP and TMPDIR.
    #
    # * I haven't tested any installer version but 15.

    homepage = "https://www.stata.com/"
    manual_download = True
    # url      = "stata"

    version("16", sha256="a13a6a92558eeb3c6cb3013c458a6777e54c21af43599df6b0a924f5f5c2d5d2")
    version("15", sha256="2486f4c7db1e7b453004c7bd3f8da40ba1e30be150613065c7b82b1915259016")

    depends_on("libpng@1.2.57", when="@15", type="run")
    depends_on("libpng@1.6.0:1.6", when="@16", type="run")

    # STATA is downloaded from user/pass protected ftp as Stata15Linux64.tar.gz
    def url_for_version(self, version):
        return "file://{0}/Stata{1}Linux64.tar.gz".format(os.getcwd(), version)

    # STATA is simple and needs really just the PATH set.
    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libpng"].prefix.lib)

    # Extracting the file provides the following:
    # ./unix/
    # ./unix/linux64/
    # ./unix/linux64/docs.taz
    # ./unix/linux64/setrwxp
    # ./unix/linux64/ado.taz
    # ./unix/linux64/inst2
    # ./unix/linux64/base.taz
    # ./unix/linux64/bins.taz
    # ./license.pdf
    # ./stata15.ico
    # ./install
    #
    # The installation scripts aren't really necessary:
    # ./install is a shell script that sets up the environment.
    # ./unix/linux64/setrwxp is a shell script that ensures permissions.
    # ./unix/linux64/inst2 is the actual installation script.
    #
    # 1. There is a markfile that is the version number. Stata uses this for
    # for doing version checks/updates.
    # echo $(date) > installed.150
    #
    # 2. Then it extracts the tar.gz files: ado.taz base.taz bins.taz docs.taz
    #
    # 3. It copies installer scripts to root directory
    # cp ./unix/linux64/setrwxp setrwxp
    # cp ./unix/linux64/inst2 inst2
    #
    # 4. Then it checks for proper permissions:
    # chmod 750 setrwxp inst2
    # ./setrwxp now
    #
    # 5. The last step has to be run manually since it is an interactive binary
    # for configuring the license key. Load the module and run:
    # $ stinit

    def install(self, spec, prefix):
        bash = which("bash")
        tar = which("tar")

        res_dir = "unix/linux64/"

        if self.spec.satisfies("@16:"):
            res_dir = "unix/linux64p/"

        # Step 1.
        x = datetime.now()
        with open("installed.150", "w") as fh:
            fh.write(x.strftime("%a %b %d %H:%M:%S %Z %Y"))

        # Step 2.
        instlist = ["ado.taz", "base.taz", "bins.taz", "docs.taz"]
        for instfile in instlist:
            tar("-x", "-z", "-f", res_dir + instfile)

        # Step 3.
        install(res_dir + "setrwxp", "setrwxp")
        install(res_dir + "inst2", "inst2")

        # Step 4. Since the install script calls out specific permissions and
        # could change in the future (or old versions) I thought it best to
        # just use it.
        bash("./setrwxp", "now")

        # Install should now be good to copy into the installation directory.
        install_tree(".", prefix)
