# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import time

from llnl.util.filesystem import touch

from spack.package import *


class ParallelPackageA(Package):
    """This is a fake vtk-m package used to demonstrate virtual package providers
    with dependencies."""

    homepage = "http://www.example.com"
    has_code = False

    depends_on("parallel-package-b")
    depends_on("parallel-package-c")

    version("1.0")

    def install(self, spec, prefix):
        print("I'm building!")
        time.sleep(2)
        print("I'm done!")

        touch(prefix.dummy_file)
