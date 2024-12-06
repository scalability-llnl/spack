# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class VisitUnv(CMakePackage):
    """This is the UNV Plug-In for VisIt."""

    # These settings are exactly those of VisIt
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    git = "https://github.com/visit-dav/visit.git"
    url = "https://github.com/visit-dav/visit/releases/download/v3.1.1/visit3.1.1.tar.gz"

    maintainers("cyrush", "cessenat")

    license("BSD-3-Clause")

    # Here we provide a local file that contains only the plugin in a flat directory
    version("local", url="file://{0}/visit-unv.tgz".format(os.getcwd()))
    # Below we copy the VisIt paths:
    version("develop", branch="develop")
    version("3.2.0", sha256="7328fd8592f9aaf17bf79ffcffd7eaec77773926b0843d9053f39c2190dbe1c0")
    version("3.1.4", sha256="be20d9acf56f0599e3c511709f48d8d3b232a57425f69d2bd1e2df1eccb84c93")
    version("3.1.1", sha256="0b60ac52fd00aff3cf212a310e36e32e13ae3ca0ddd1ea3f54f75e4d9b6c6cf0")
    version("3.0.1", sha256="a506d4d83b8973829e68787d8d721199523ce7ec73e7594e93333c214c2c12bd")
    version("2.13.3", sha256="cf0b3d2e39e1cd102dd886d3ef6da892733445e362fc28f24d9682012cccf2e5")
    version("2.13.0", sha256="716644b8e78a00ff82691619d4d1e7a914965b6535884890b667b97ba08d6a0f")
    version("2.12.3", sha256="2dd351a291ee3e79926bc00391ca89b202cfa4751331b0fdee1b960c7922161f")
    version("2.12.2", sha256="55897d656ac2ea4eb87a30118b2e3963d6c8a391dda0790268426a73e4b06943")
    version("2.10.3", sha256="05018215c4727eb42d47bb5cc4ff937b2a2ccaca90d141bc7fa426a0843a5dbc")
    version("2.10.2", sha256="89ecdfaf197ef431685e31b75628774deb6cd75d3e332ef26505774403e8beff")
    version("2.10.1", sha256="6b53dea89a241fd03300a7a3a50c0f773e2fb8458cd3ad06816e9bd2f0337cd8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("visit")

    extends("visit")

    build_targets = ["VERBOSE=1"]
    phases = ["cmake", "build"]
    extname = "unv"

    @property
    def root_cmakelists_dir(self):
        if "@local" not in self.spec:
            return join_path("src", "databases", self.extname)
        else:
            return "."

    @property
    def build_directory(self):
        return self.root_cmakelists_dir

    @run_before("cmake")
    def run_xml2cmake(self):
        visit = self.spec["visit"]
        args = ["-v", str(visit.version), "-clobber", "-public", self.extname + ".xml"]
        with working_dir(self.root_cmakelists_dir):
            # Regenerate the public cmake files
            if os.path.exists("CMakeLists.txt"):
                os.unlink("CMakeLists.txt")
            which("xml2cmake")(*args)
            # spack extension activate : alter VISIT_PLUGIN_DIR ;
            # xml2cmake should have set it to visit prefix but it can
            # happen the directory is an alias.
            # In that case we match version/smth/plugins.
            mstr = None
            mstr1 = r"^SET[(]VISIT_PLUGIN_DIR\s+\"{0}(.+)\"[)]".format(visit.prefix)
            mstr2 = r"^SET[(]VISIT_PLUGIN_DIR\s+\".+({0}.+?{1})\"[)]".format(
                join_path(os.sep, visit.version, ""), join_path(os.sep, "plugins")
            )
            with open("CMakeLists.txt", "r") as file:
                for line in file:
                    if re.search(mstr1, line):
                        mstr = mstr1
                    elif re.search(mstr2, line):
                        mstr = mstr2
            if mstr is not None:
                filter_file(
                    mstr, r'SET(VISIT_PLUGIN_DIR "{0}\1")'.format(prefix), "CMakeLists.txt"
                )
