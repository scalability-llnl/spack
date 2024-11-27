# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ack(Package):
    """ack 2.14 is a tool like grep, optimized for programmers.

    Designed for programmers with large heterogeneous trees of
    source code, ack is written purely in portable Perl 5 and takes
    advantage of the power of Perl's regular expressions."""

    homepage = "https://beyondgrep.com/"
    url = "https://beyondgrep.com/ack-2.14-single-file"

    license("Artistic-2.0")

    version(
        "2.22",
        sha256="fd0617585b88517a3d41d3d206c1dc38058c57b90dfd88c278049a41aeb5be38",
        expand=False,
    )
    version(
        "2.18",
        sha256="6e41057c8f50f661d800099471f769209480efa53b8a886969d7ec6db60a2208",
        expand=False,
    )
    version(
        "2.16",
        sha256="7f39f08ebb78ed160a41293d7f42ff1bdcdaf57aee859bc4c4888bdf4abee7f2",
        expand=False,
    )
    version(
        "2.14",
        sha256="1d203cfbc52ce8f49e3992be1cd3e4d7d5dfb7daa3739e8628aa9858ccc5b9df",
        expand=False,
    )

    depends_on("perl")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        ack_source = f"ack-{self.version}-single-file"
        ack_installed = join_path(prefix.bin, "ack")

        # install source
        install(ack_source, ack_installed)
        set_executable(ack_installed)

        # rewrite the script's #! line to call the perl dependency
        shbang = "#!" + spec["perl"].command.path
        filter_file(r"^#!/usr/bin/env perl", shbang, ack_installed)
