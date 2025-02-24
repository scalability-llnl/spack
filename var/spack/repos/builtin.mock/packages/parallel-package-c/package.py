# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import time

from llnl.util.filesystem import touch

from spack.package import *


class ParallelPackageC(Package):
    """This is a fake vtk-m package used to demonstrate virtual package providers
    with dependencies."""

    homepage = "http://www.example.com"
    has_code = False

    version("1.0")

    def install(self, spec, prefix):
        print("Package 3 building!")
        time.sleep(2)
        print("Ideally shouldnt get here and it should fail")

        touch(prefix.dummy_file)
