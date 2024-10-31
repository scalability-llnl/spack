# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Daligner(MakefilePackage):
    """Daligner: The Dazzler "Overlap" Module."""

    homepage = "https://github.com/thegenemyers/DALIGNER"
    url = "https://github.com/thegenemyers/DALIGNER/archive/V1.0.tar.gz"

    version("1.0", sha256="2fb03616f0d60df767fbba7c8f0021ec940c8d822ab2011cf58bd56a8b9fb414")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        kwargs = {"ignore_absent": False, "backup": False, "string": True}
        makefile.filter("cp $(ALL) ~/bin", "cp $(ALL) {0}".format(prefix.bin), **kwargs)
        # He changed the Makefile in commit dae119.
        # You'll need this instead if/when he cuts a new release
        # or if you try to build from the tip of master.
        # makefile.filter('DEST_DIR = .*',
        #                'DEST_DIR = {0}'.format(prefix.bin))
        # or pass DEST_DIR in to the make

    @run_before("install")
    def make_prefix_dot_bin(self):
        mkdir(prefix.bin)
