# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Targetp(Package):
    """TargetP predicts the subcellular location of eukaryotic protein sequences.

    Note: A manual download is required for TargetP.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.cbs.dtu.dk/services/TargetP/"
    url = "file://{0}/targetp-1.1b.Linux.tar.gz".format(os.getcwd())
    manual_download = True

    version("1.1b", md5="80233d0056e11abfd22a4ce73d1808c6")

    depends_on("perl", type="run")
    depends_on("awk", type="run")
    depends_on("chlorop")
    depends_on("signalp")

    def patch(self):
        targetp = FileFilter("targetp")
        targetp.filter("TARGETP=", "#TARGETP=")
        targetp.filter("CHLOROP=/usr/cbs/bio/bin/chlorop", self.spec["chlorop"].prefix.bin.chlorop)
        targetp.filter("SIGNALP=/usr/cbs/bio/bin/signalp", self.spec["signalp"].prefix.signalp)
        targetp.filter("TMP=/scratch", "TMP=/tmp")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("etc", prefix.etc)
        install_tree("how", prefix.how)
        install_tree("test", prefix.test)
        install_tree("tmp", prefix.tmp)
        install("targetp", prefix.targetp)

    def setup_run_environment(self, env):
        env.set("TARGETP", self.prefix)
        env.prepend_path("PATH", self.prefix)
