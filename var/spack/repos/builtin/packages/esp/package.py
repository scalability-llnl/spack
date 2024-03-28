# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import os

from spack.package import *
from spack.util.environment import EnvironmentModifications

_versions = {
    "1.24": {
        "Linux-x86_64": (
            "44b5df419195d310546050481e6c929d42135e61e6254f453a8feda1ef44008e",
            "https://acdl.mit.edu/ESP/PreBuilts/ESP124-linux-x86_64.tgz",
        )
    },
}

class Esp(Package):
    """MIT's Engineering Sketch Pad"""

    homepage = "https://acdl.mit.edu/ESP"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    depends_on("libxml2")
    depends_on("gmake", type="build")

    def install(self, spec, prefix):

        # Patch a few Makefiles to for some rpath issues
        #
        # This:
        #     PATH=$(PYTHONLPATH:-L%=-Wl,-rpath %)
        # to:
        #     PATH=$(PYTHONLPATH:-L%=-Wl,-rpath,%)
        #
        # I.e. use a comma instead of a space after -rpath):
        files=[ 'EngSketchPad/src/CAPS/aim/fun3d/Makefile',
                'EngSketchPad/src/CAPS/aim/abaqus/Makefile',
                'EngSketchPad/src/OpenCSM/serveESP.make' ]
        for file in files:
            makefile = FileFilter(file)
            makefile.filter("-rpath %", "-rpath,%")

        # This copies the source to the final installion location
        install_tree(".", prefix)

        bash = which("bash")

        # This gets the full path to the bash script in this directory
        script=join_path(os.path.dirname(__file__), "finish_setup.sh")

        # Run the setup in the final location.  This is neceessary becase
        # ESP's scripts reconfigure env vars and other items with full
        # paths to the current location.  So we can't run this in the
        # staging area and then transfer.
        with working_dir(prefix):
            bash("setup.sh") # Run the setup script that comes with ESP
            bash(script)     # Run the setup to finish the process

    def setup_run_environment(self, env):
        filename = self.prefix.join("EngSketchPad").join("ESPenv.sh")
        env.extend(EnvironmentModifications.from_sourcing_file(filename))
