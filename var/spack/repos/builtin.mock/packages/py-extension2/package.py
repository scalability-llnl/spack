# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class PyExtension2(PythonPackage):
    """A package which extends python. It also depends on another
    package which extends the same package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/extension2-1.0.tar.gz"

    # Override settings in base class
    maintainers = []

    extends("python")
    depends_on("py-extension1", type=("build", "run"))

    version("1.0", md5="00000000000000000000000000000210")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with open(os.path.join(prefix.bin, "py-extension2"), "w+") as fout:
            fout.write(str(spec.version))
