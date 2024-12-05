# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gnat(Package):
    """The GNAT Ada compiler. Ada is a modern programming language designed
    for large, long-lived applications - and embedded systems in particular
    - where reliability and efficiency are essential."""

    homepage = "https://libre.adacore.com/tools/gnat-gpl-edition/"

    # NOTE: This is a binary installer intended to bootstrap GCC's Ada compiler

    # There may actually be a way to install GNAT from source. If you go to
    # the GNAT Download page: https://libre.adacore.com/download/
    # select "Free Software or Academic Development", select your platform,
    # expand GNAT Ada, and expand Sources, you'll see links to download the
    # source code for GNAT and all of its dependencies. Most of these
    # dependencies are already in Spack.

    # This is the GPL release for Linux x86-64
    version(
        "2016",
        sha256="d083c01e054d0aeda7c67967306cfa5a8df12268664f9098a2d9b331aa24dfe7",
        extension="tar.gz",
        url="http://mirrors.cdn.adacore.com/art/5739cefdc7a447658e0b016b",
    )

    def install(self, spec, prefix):
        make("ins-all", "prefix={0}".format(prefix))
