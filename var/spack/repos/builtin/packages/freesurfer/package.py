# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Freesurfer(Package):
    """Freesurfer is an open source software suite for processing and analyzing
    (human) brain MRI images."""

    homepage = "https://freesurfer.net/"

    # A license is required, but is free to obtain.
    license_required = True
    license_files = [".license"]

    maintainers("robgics")

    version("7.4.1", sha256="313a96caeb246c5985f483633b5cf43f86ed8f7ccc6d6acfac8eedb638443010")
    version("7.4.0", sha256="6b65c2edf3b88973ced0324269a88966c541f221b799337c6570c38c2f884431")
    version("7.3.2", sha256="58518d3ee5abd2e05109208aed2eef145c4e3b994164df8c4e0033c1343b9e56")
    version("7.2.0", sha256="4cca78602f898bf633428b9d82cbb9b07e3ab97a86c620122050803779c86d62")
    version("7.1.1", sha256="6098b166fee8644f44f9ec88f3ffe88d05f2bc033cca60443e99e3e56f2e166b")
    version("7.1.0", sha256="1b8f26fe5c712433ddb74c47fe1895ed1d9fbff46cfae8aaae2697cb65ae8840")

    depends_on("mesa-glu")
    depends_on("qt")
    depends_on("tcsh")
    depends_on("bc")
    depends_on("perl")

    def url_for_version(self, version):
        return "https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/{0}/freesurfer-linux-centos7_x86_64-{1}.tar.gz".format(
            version, version
        )

    def setup_run_environment(self, env):
        source_file = join_path(self.prefix, "SetUpFreeSurfer.sh")
        env.prepend_path("PATH", self.prefix.bin)
        env.set("FREESURFER_HOME", self.prefix)
        env.set("SUBJECTS_DIR", join_path(self.prefix, "subjects"))
        env.set("FUNCTIONALS_DIR", join_path(self.prefix, "sessions"))
        env.append_path("PERL5LIB", join_path(self.prefix, "mni/share/perl5"))
        env.append_path("PATH", join_path(self.prefix, "mni/bin"))
        env.extend(EnvironmentModifications.from_sourcing_file(source_file))

    def install(self, spec, prefix):
        scripts = ["sources.csh", "SetUpFreeSurfer.csh"]
        scripts.extend(glob.glob("bin/*"))
        scripts.extend(glob.glob("subjects/**/*", recursive=True))
        scripts.extend(glob.glob("fsfast/bin/*", recursive=True))
        scripts.extend(glob.glob("mni/bin/*", recursive=True))
        for s in scripts:
            if os.path.isfile(s):
                filter_file(r"(\/usr)?(\/local?)\/bin\/tcsh", "/usr/bin/env -S tcsh", s)
                filter_file(r"(\/usr)?(\/local?)\/bin\/csh", "/usr/bin/env -S csh", s)
                filter_file(r"(\/usr)?(\/local)?\/bin\/perl", "/usr/bin/env -S perl", s)
        install_tree(".", prefix)
