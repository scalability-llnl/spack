# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libszip(AutotoolsPackage):
    """Szip is an implementation of the extended-Rice lossless
     compression algorithm.

    It provides lossless compression of scientific data, and is
    provided with HDF software products.
    """

    homepage = "https://support.hdfgroup.org/doc_resource/SZIP/"
    url = "https://support.hdfgroup.org/ftp/lib-external/szip/2.1.1/src/szip-2.1.1.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/lib-external/szip"
    list_depth = 3

    provides("szip")

    version("2.1.1", sha256="21ee958b4f2d4be2c9cabfa5e1a94877043609ce86fde5f286f105f7ff84d412")
    version("2.1", sha256="a816d95d5662e8279625abdbea7d0e62157d7d1f028020b1075500bf483ed5ef")

    depends_on("c", type="build")  # generated

    @property
    def libs(self):
        shared = "static" not in self.spec.last_query.extra_parameters

        libs = find_libraries("libsz", root=self.prefix, shared=shared, recursive=True)

        if not libs:
            msg = "Unable to recursively locate {0} {1} libraries in {2}"
            raise spack.error.NoLibrariesError(
                msg.format("shared" if shared else "static", self.spec.name, self.spec.prefix)
            )
        return libs

    def configure_args(self):
        return ["--enable-production", "--enable-shared", "--enable-static", "--enable-encoding"]
