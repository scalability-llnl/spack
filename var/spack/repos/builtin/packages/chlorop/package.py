# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Chlorop(Package):
    """Chlorop predicts the presence of chloroplast transit peptides
    in protein sequences and the location of potential cTP cleavage
    sites. You will need to obtain the tarball by visiting the
    URL and completing the form. You can then either run spack
    install with the tarball in the directory, or add it to a
    mirror. You will need to set the CHLOROTMP environment variable
    to the full path of the directory you want chlorop to use as
    a temporary directory."""

    homepage = "https://www.cbs.dtu.dk/services/ChloroP/"
    url = "file://{0}/chlorop-1.1.Linux.tar.gz".format(os.getcwd())
    manual_download = True

    version("1.1", sha256="eb0ba6b28dfa735163ad5fc70e30139e46e33f6ae27f87666a7167a4ac5f71d9")

    depends_on("awk", type="run")
    patch("chlorop.patch")

    def install(self, spec, prefix):
        os.rename("chlorop", "bin/chlorop")
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.set("CHLOROP", self.prefix)
