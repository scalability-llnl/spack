# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nb(Package):
    """
    nb is a command line and local web note‑taking, bookmarking, archiving,
    and knowledge base application.
    """

    homepage = "https://xwmx.github.io/nb/"
    url = "https://github.com/xwmx/nb/archive/refs/tags/7.12.1.tar.gz"

    maintainers("taliaferro")

    license("AGPL-3.0", checked_by="taliaferro")

    version("7.12.1", sha256="c9b30448751dd726469ed3fde29e618c5747eb4a16ceaaf86d773989a6cf13f3")

    depends_on("git")
    depends_on("bash")

    def patch(self):
        filter_file(
            r"^#!\s?.*bash",
            "#!{}".format(self.spec["bash"].command.path),
            "nb",
            "bin/bookmark",
            "bin/notes",
            "etc/nb-completion.bash",
        )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix + "/share/bash-completion/completions")
        install("nb", join_path(prefix, "bin/nb"))
        install("bin/notes", join_path(prefix, "bin/notes"))
        install("bin/bookmark", join_path(prefix, "bin/bookmark"))
        install(
            "etc/nb-completion.bash", join_path(prefix, "share/bash-completion/completions/nb")
        )
