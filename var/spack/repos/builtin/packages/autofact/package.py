# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Autofact(Package):
    """An Automatic Functional Annotation and Classification Tool"""

    homepage = "https://megasun.bch.umontreal.ca/Software/AutoFACT.htm"
    url = "https://megasun.bch.umontreal.ca/Software/AutoFACT_v3_4.tar"

    version("3_4", sha256="1465d263b19adb42f01f6e636ac40ef1c2e3dbd63461f977b89da9493fe9c6f4")

    depends_on("perl", type="run")
    depends_on("perl-bioperl", type="run")
    depends_on("perl-io-string", type="run")
    depends_on("perl-libwww-perl", type="run")
    depends_on("blast-legacy", type="run")

    def patch(self):
        with working_dir("scripts"):
            files = glob.iglob("*.pl")
            for file in files:
                change = FileFilter(file)
                change.filter("usr/bin/perl", "usr/bin/env perl")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.scripts)
        env.set("PATH2AUTOFACT", self.prefix)
