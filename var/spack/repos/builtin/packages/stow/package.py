# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stow(AutotoolsPackage, GNUMirrorPackage):
    """GNU Stow: a symlink farm manager

    GNU Stow is a symlink farm manager which takes distinct
    packages of software and/or data located in separate
    directories on the filesystem, and makes them appear to be
    installed in the same place."""

    homepage = "https://www.gnu.org/software/stow/"
    gnu_mirror_path = "stow/stow-2.2.2.tar.bz2"

    license("GPL-3.0-or-later")

    version("2.4.0", sha256="a7bac673daa246cf54ffb48a113eadd204a615630e76b53b5f64d81a275b77b3")
    version("2.3.1", sha256="26a6cfdfdaca0eea742db5487798c15fcd01889dc86bc5aa62614ec9415a422f")
    version("2.2.2", sha256="a0022034960e47a8d23dffb822689f061f7a2d9101c9835cf11bf251597aa6fd")
    version("2.2.0", sha256="86bc30fe1d322a5c80ff3bd7580c2758149aad7c3bbfa18b48a9d95c25d66b05")
    version("2.1.3", sha256="2dff605c801fee9fb7d0fef6988bbb8a0511fad469129b20cae60e0544ba1443")
    version("2.1.2", sha256="dda4231dab409d906c5de7f6a706a765e6532768ebbffe34e1823e3371f891f9")
    version("2.1.1", sha256="8bdd21bb2ef6edf5812bf671e64cdd584d92d547d932406cef179646ea6d1998")
    version("2.1.0", sha256="f0e909034fd072b1f5289abb771133d5c4e88d82d4da84195891c53d9b0de5ca")

    depends_on("perl@5.6.1:")
