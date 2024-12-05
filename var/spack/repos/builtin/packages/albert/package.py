# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Albert(MakefilePackage):
    """Albert is an interactive program to assist the
    specialist in the study of nonassociative algebra."""

    homepage = "https://people.cs.clemson.edu/~dpj/albertstuff/albert.html"
    url = "https://github.com/kentavv/Albert/archive/v4.0a_opt4.tar.gz"

    version("4.0a_opt4", sha256="80b9ee774789c9cd123072523cfb693c443c3624708a58a5af177a51f36b2c79")
    version("4.0a", sha256="caf49e24fb9bf2a09053d9bf022c4737ffe61d62ce9c6bc32aa03dded2a14913")

    depends_on("cxx", type="build")  # generated

    depends_on("readline")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("albert", join_path(prefix.bin))
