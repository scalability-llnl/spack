# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack.package import *


class Symly(Package):
    """A toy package full of symlinks."""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    def install(self, spec, prefix):
        symly_c = """
#include <stdio.h>

int main() {
    printf("I'm just here to give the build system something to do...");
    return 0;
}
"""
        mkdirp("%s/symly" % self.stage.source_path)
        with open("%s/symly/symly.c" % self.stage.source_path, "w") as f:
            f.write(symly_c)
        gcc = which("/usr/bin/gcc")
        if sys.platform == "darwin":
            gcc = which("/usr/bin/clang")
        mkdirp(prefix.bin)
        mkdirp(prefix.lib64)
        gcc("-o", "symly.bin", "symly/symly.c")
        print("prefix.bin", prefix.bin)
        copy("symly.bin", "%s/symly" % prefix.bin)
        # create a symlinked file.
        os.symlink("%s/symly" % prefix.bin, "%s/symly" % prefix.lib64)
        # Create a symlinked directory.
        os.symlink(prefix.bin, prefix.include)
