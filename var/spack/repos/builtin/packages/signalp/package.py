# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Signalp(Package):
    """SignalP predicts the presence and location of signal peptide cleavage
    sites in amino acid sequences from different organisms: Gram-positive
    bacteria, Gram-negative bacteria, and eukaryotes.
    Note: A manual download is required for SignalP.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.cbs.dtu.dk/services/SignalP/"
    url = "file://{0}/signalp-4.1f.Linux.tar.gz".format(os.getcwd())
    manual_download = True

    version("4.1f", md5="a9aeb66259202649c959846f3f4d9744")

    depends_on("perl", type=("build", "run"))
    depends_on("gnuplot")

    def patch(self):
        edit = FileFilter("signalp")
        edit.filter("ENV{SIGNALP} = .*", "ENV{SIGNALP} = '%s'" % self.prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.share.man)
        install("signalp", prefix)
        install("signalp.1", prefix.share.man)
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("syn", prefix.syn)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
