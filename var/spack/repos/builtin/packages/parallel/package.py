# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.hooks.sbang import filter_shebang
from spack.package import *


class Parallel(AutotoolsPackage, GNUMirrorPackage):
    """GNU parallel is a shell tool for executing jobs in parallel using
    one or more computers. A job can be a single command or a small
    script that has to be run for each of the lines in the input.
    """

    homepage = "https://www.gnu.org/software/parallel/"
    gnu_mirror_path = "parallel/parallel-20220522.tar.bz2"

    license("GPL-3.0-or-later", checked_by="wdconinc")

    version("20240822", sha256="d7bbd95b7631980b172be04cbd2138d5f7d8c063d6da5ad8f9f70dfd88c8309d")
    version("20220522", sha256="bb6395f8d964e68f3bdb26a764d3c48b69bc5b759a92ac3ab2bd1895c7fa8c1f")
    version("20220422", sha256="96e4b73fff1302fc141a889ae43ab2e93f6c9e86ac60ef62ced02dbe70b73ca7")
    version("20220322", sha256="df93ccf6a9f529ad2126b7042aef0486603e938c77b405939c41702d38a4e6d8")
    version("20220222", sha256="f81682b863ead7fb9a114754001e9286f954550a57a3cf36c9003a8047a6a445")
    version("20220122", sha256="b8221a21412bca572ad8445b7981dfd625a3c6d48772cda468dfb5b886337e00")
    version("20210922", sha256="dedca94fc41f2054dbadd9b8361e56015fc8af5d1961c1b982b63e6d86494d66")
    version("20200822", sha256="9654226a808392c365b1e7b8dea91bf4870bc4f306228d853eb700679e21be09")
    version("20190222", sha256="86b1badc56ee2de1483107c2adf634604fd72789c91f65e40138d21425906b1c")
    version("20170322", sha256="f8f810040088bf3c52897a2ee0c0c71bd8d097e755312364b946f107ae3553f6")
    version("20170122", sha256="417e83d9de2fe518a976fcff5a96bffe41421c2a57713cd5272cc89d1072aaa6")
    version("20160422", sha256="065a8f471266361218a9eb45c5f8ab995d73b181cc1180600ee08cc768c9ac42")
    version("20160322", sha256="6430f649ec07243645c955e8d6bee6da1df2e699b1e49b185946d1ab38731b08")

    def check(self):
        # The Makefile has a 'test' target, but it does not work
        make("check")

    depends_on("perl", type=("build", "run"))

    @run_before("install")
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
        can fix up the path to the perl binary.
        """
        perl = self.spec["perl"].command
        kwargs = {"ignore_absent": False, "backup": False, "string": False}

        with working_dir("src"):
            match = "^#!/usr/bin/env perl|^#!/usr/bin/perl.*"
            substitute = f"#!{perl}"
            files = ["parallel", "niceload", "parcat", "sql"]
            filter_file(match, substitute, *files, **kwargs)
            # Since scripts are run during installation, we need to add sbang
            for file in files:
                filter_shebang(file)
