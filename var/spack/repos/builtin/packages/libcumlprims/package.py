# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcumlprims(Package):
    """libcuMLPrims library"""

    homepage = "https://rapids.ai"
    url = "https://anaconda.org/nvidia/libcumlprims/0.15.0/download/linux-64/libcumlprims-0.15.0-cuda11.0_gdbd0d39_0.tar.bz2"

    version(
        "0.15.0-cuda11.0_gdbd0d39_0",
        sha256="0edc55767f06f533fbff7a0fecaf6e6d4f82eec39604b3874a07b5609f79ece8",
    )
    version(
        "0.15.0-cuda10.2_gdbd0d39_0",
        sha256="b7a8740de0d15380829f42fcb078567e73ab7d29b14be073376153bf2d8ec945",
    )
    version(
        "0.15.0-cuda10.1_gdbd0d39_0",
        sha256="f055f904b5ef67995869b0bc648d9fe30839b08e77cb335573bf9f1c816d4d9b",
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cuda@11.0.0:11.0", when="@0.15.0-cuda11.0_gdbd0d39_0")
    depends_on("cuda@10.2.0:10.2", when="@0.15.0-cuda10.2_gdbd0d39_0")
    depends_on("cuda@10.1.0:10.1", when="@0.15.0-cuda10.1_gdbd0d39_0")

    @property
    def headers(self):
        headers = find_headers("*", self.prefix.include, recursive=True)
        headers.directories = [self.prefix.include, self.prefix.include.cumlprims]
        return headers

    def url_for_version(self, version):
        url = "https://anaconda.org/nvidia/libcumlprims/{0}/download/linux-64/libcumlprims-{1}.tar.bz2"
        return url.format(version.up_to(3), version)

    def install(self, spec, prefix):
        install_tree(".", self.prefix)
