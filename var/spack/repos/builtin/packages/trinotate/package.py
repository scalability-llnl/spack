# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Trinotate(Package):
    """Trinotate is a comprehensive annotation suite designed for
    automatic functional annotation of transcriptomes, particularly
    de novo assembled transcriptomes, from model or non-model organisms"""

    homepage = "https://trinotate.github.io/"
    url = "https://github.com/Trinotate/Trinotate/archive/Trinotate-v3.1.1.tar.gz"

    license("BSD-3-Clause")

    version("3.2.2", sha256="1c41258a544cccb332f77b73f7397b457d5f3d7ce0038505369aeecc1e0650c2")
    version("3.1.1", sha256="f8af0fa5dbeaaf5a085132cd4ac4f4206b05cc4630f0a17a672c586691f03843")

    depends_on("trinity", type="run")
    depends_on("transdecoder", type="run")
    depends_on("sqlite", type="run")
    depends_on("ncbi-rmblastn", type="run")
    depends_on("hmmer", type="run")
    depends_on("perl", type="run")
    depends_on("lighttpd", type="run")
    depends_on("perl-dbi", type="run")
    depends_on("perl-cgi", type="run")
    depends_on("perl-dbd-sqlite", type="run")

    def patch(self):
        with working_dir(join_path(self.stage.source_path, "admin/util")):
            perlscripts = glob.glob("*.pl")
            filter_file("#!/usr/bin/perl", "#!/usr/bin/env perl", *perlscripts)

        # trinotate web generates a config on run but puts it in a bad place
        # this causes issues with permissions; we hack the source to keep it
        # in the calling user's homedir

        filter_file(
            '"$FindBin::RealBin/TrinotateWeb.conf/lighttpd.conf.port',
            '$ENV{"HOME"} . "/.trinotate_lighttpd.conf.port',
            "run_TrinotateWebserver.pl",
            string=True,
        )

    def install(self, spec, prefix):
        # most of the perl modules have local deps, install the whole tree
        mkdirp(prefix.lib)
        install_tree(".", join_path(prefix.lib, "trinotate"))

        mkdirp(prefix.bin)
        os.symlink(
            join_path(prefix.lib, "trinotate/Trinotate"), join_path(prefix.bin, "Trinotate")
        )

        os.symlink(
            join_path(prefix.lib, "trinotate/run_TrinotateWebserver.pl"),
            join_path(prefix.bin, "run_TrinotateWebserver.pl"),
        )
