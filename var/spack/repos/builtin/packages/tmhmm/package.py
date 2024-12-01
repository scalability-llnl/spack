# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Tmhmm(Package):
    """Transmembrane helices in proteins

    Note: A manual download is required for TMHMM.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.cbs.dtu.dk/cgi-bin/nph-sw_request?tmhmm"
    url = "file://{0}/tmhmm-2.0c.Linux.tar.gz".format(os.getcwd())
    manual_download = True

    version("2.0c", md5="359db0c4ecf84d1ade5786abe844d54e")

    depends_on("perl", type="run")

    def patch(self):
        with working_dir("bin"):
            tmhmm = FileFilter("tmhmmformat.pl")
            tmhmm.filter("#!/usr/local/bin/perl -w", "#!/usr/bin/env perl")
            tmhmm = FileFilter("tmhmm")
            tmhmm.filter("#!/usr/local/bin/perl", "#!/usr/bin/env perl")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
