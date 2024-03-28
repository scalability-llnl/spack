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

    #depends_on("libxml2", type="build")
    depends_on("libxml2")
    depends_on("gmake", type="build")

    def install(self, spec, prefix):

        # Patch a few Makefiles to for some rpath issues
        # This line:
        #     PATH=$(PYTHONLPATH:-L%=-Wl,-rpath %)
        # to:
        #     PATH=$(PYTHONLPATH:-L%=-Wl,-rpath,%)
        #
        # should look like this (comma instead of space after -rpath):
        files=[ 'EngSketchPad/src/CAPS/aim/fun3d/Makefile',
                'EngSketchPad/src/CAPS/aim/abaqus/Makefile',
                'EngSketchPad/src/OpenCSM/serveESP.make' ]
        for file in files:
            makefile = FileFilter(file)
            makefile.filter("-rpath %",  "-rpath,%")

        # Patch a few more Makefiles to look for the right xml2-config
        #files=[ 'EngSketchPad/src/CAPS/aim/cart3d/xddm/Makefile',
        #        'EngSketchPad/src/CAPS/aim/cart3d/Makefile']
        #print(f"spec = {spec}")
        #print(f"spec['libxml2'] = {spec['libxml2']}")
        #print(f"spec['libxml2'].prefix = {spec['libxml2'].prefix}")
        #for file in files:
        #    makefile = FileFilter(file)
        #    makefile.filter("xml2-config",  f"{spec['libxml2'].prefix}/bin/xml2-config" )
        #    f'-DCMAKE_C_COMPILER={spec["mpi"].mpicc}',

        # This copies the source to the prefix
        install_tree(".", prefix)


        bash = which("bash")
        script=join_path(os.path.dirname(__file__), "finish_setup.sh")

        with working_dir(prefix):
            bash("setup.sh")
            bash(script)

        #with working_dir(prefix.join("EngSketchPad").join("src")):
        #    make()

    def setup_run_environment(self, env):
        filename = self.prefix.join("EngSketchPad").join("ESPenv.sh")
        env.extend(EnvironmentModifications.from_sourcing_file(filename))
