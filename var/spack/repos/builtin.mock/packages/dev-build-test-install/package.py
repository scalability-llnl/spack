# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DevBuildTestInstall(MakefilePackage):
    homepage = "example.com"
    url = "fake.com"

    version("0.0.0", sha256="0123456789abcdef0123456789abcdef")

    filename = "dev-build-test-file.txt"
    original_string = "This file should be edited"
    replacement_string = "This file has been edited"

    def edit(self, spec, prefix):
        with open(self.filename, "r+") as f:
            assert f.read() == self.original_string
            f.seek(0)
            f.truncate()
            f.write(self.replacement_string)

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        install(self.filename, prefix)
