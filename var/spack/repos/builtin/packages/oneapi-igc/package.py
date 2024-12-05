# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OneapiIgc(Package):
    """The Intel Graphics Compiler for OpenCL is an LLVM based compiler
    for OpenCL targeting Intel Gen graphics hardware architecture.

    """

    homepage = "https://github.com/intel/intel-graphics-compiler"
    has_code = False

    maintainers("rscohn2")

    version("1.0.10409")
    version("1.0.8744")
    version("1.0.8517")

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )

    @property
    def libs(self):
        return find_libraries(["libigc"], root=self.prefix, recursive=True)
