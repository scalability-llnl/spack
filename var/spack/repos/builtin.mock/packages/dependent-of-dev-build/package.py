# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DependentOfDevBuild(Package):
    homepage = "example.com"
    url = "fake.com"

    version("0.0.0", sha256="0123456789abcdef0123456789abcdef")

    depends_on("dev-build-test-install")

    def install(self, spec, prefix):
        with open(prefix.filename, "w") as f:
            f.write("This file is installed")
