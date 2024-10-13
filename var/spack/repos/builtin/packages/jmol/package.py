# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Jmol(Package):
    """Jmol: an open-source Java viewer for chemical structures in 3D
    with features for chemicals, crystals, materials and biomolecules."""

    homepage = "https://jmol.sourceforge.net/"
    url = "https://sourceforge.net/projects/jmol/files/Jmol/Version%2014.8/Jmol%2014.8.0/Jmol-14.8.0-binary.tar.gz"

    license("LGPL-2.1-or-later")

    version("14.31.0", sha256="eee0703773607c8bd6d51751d0d062c3e10ce44c11e1d7828e4ea3d5f710e892")
    version("14.8.0", sha256="8ec45e8d289aa0762194ca71848edc7d736121ddc72276031a253a3651e6d588")

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/jmol/files/Jmol/Version%20{0}/Jmol%20{1}/Jmol-{1}-binary.tar.gz"
        return url.format(version.up_to(2), version)

    depends_on("java", type="run")

    def install(self, spec, prefix):
        if os.path.exists("jmol-{0}".format(self.version)):
            # tar ball contains subdir with different versions
            install_tree("jmol-{0}".format(self.version), prefix)
        else:
            # no subdirs - tarball was unpacked in spack-src
            install_tree("./", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
        env.set("JMOL_HOME", self.prefix)
        env.prepend_path("PATH", self.spec["java"].prefix.bin)
