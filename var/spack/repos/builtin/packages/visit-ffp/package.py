# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class VisitFfp(CMakePackage):
    """This is the FFP Plug-In for VisIt.
    Can be installed after VisIt is installed with/without the STRIPACK library.
    """

    # These settings are exactly those of VisIt
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    git = "https://github.com/visit-dav/visit.git"
    url = "https://github.com/visit-dav/visit/releases/download/v3.1.1/visit3.1.1.tar.gz"

    maintainers("cyrush", "cessenat")

    license("BSD-3-Clause")

    # Here we provide a local file that contains only the plugin in a flat directory
    version("local", url="file://{0}/visit-ffp.tgz".format(os.getcwd()))
    # Below we copy the VisIt paths, ffp first shipment is with VisIt 3
    version("develop", branch="develop")
    version("3.2.0", sha256="7328fd8592f9aaf17bf79ffcffd7eaec77773926b0843d9053f39c2190dbe1c0")
    version("3.1.4", sha256="be20d9acf56f0599e3c511709f48d8d3b232a57425f69d2bd1e2df1eccb84c93")
    version("3.1.1", sha256="0b60ac52fd00aff3cf212a310e36e32e13ae3ca0ddd1ea3f54f75e4d9b6c6cf0")
    version("3.0.1", sha256="a506d4d83b8973829e68787d8d721199523ce7ec73e7594e93333c214c2c12bd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("stripack", default=True, description="Enable STRIPACK unit sphere Delaunay meshing")

    depends_on("cmake", type="build")
    depends_on("stripack", when="+stripack")
    depends_on("visit")

    extends("visit")

    build_targets = ["VERBOSE=1"]
    phases = ["cmake", "build"]
    extname = "ffp"

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
