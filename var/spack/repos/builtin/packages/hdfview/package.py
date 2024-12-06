# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Hdfview(Package):
    """HDFView is a visual tool written in Java for browsing
    and editing HDF (HDF5 and HDF4) files."""

    homepage = "https://www.hdfgroup.org/downloads/hdfview/"
    url = "https://support.hdfgroup.org/ftp/HDF5/releases/HDF-JAVA/hdfview-3.1.4/src/hdfview-3.1.4.tar.gz"

    version("3.3.0", sha256="0916161861c21fa8dd354b445b48eff5a53d80a5c0b383e79eb64b7b108e2430")
    version("3.2.0", sha256="d3c0deff2cbd959508c4da9c712da72fb204ff6818a3434f00a7071f8e8cf2b8")
    version("3.1.4", sha256="898fcd5227d4e7b697efde5e5a969405f96b72517f9dfbdbdce2991290fd56a0")
    version("3.1.1", sha256="1cfd127ebb4c3b0ab1cfe54649a410fc7a1c2d73f45564697d3729f4aa6b0ba3")
    version(
        "3.0",
        sha256="e2a16d3842d8947f3d4f154ee9f48a106c7f445914a9e626a53976d678a0e934",
        url="https://s3.amazonaws.com/hdf-wordpress-1/wp-content/uploads/manual/HDFView/hdfview-3.0.tar.gz",
    )

    # unknown flag: --ignore-missing-deps
    patch("fix_build.patch", when="@3.1.1")

    depends_on("ant", type="build")
    depends_on("hdf5 +java")
    depends_on("hdf +java -external-xdr +shared")

    depends_on("hdf5@1.10", when="@:3.1")
    depends_on("hdf5@1.12:", when="@3.2")
    depends_on("hdf5@1.14:", when="@3.3:")

    def install(self, spec, prefix):
        ant = which("ant")
        ant("-Dbuild.debug=false", "deploy")

        dir_version = os.listdir("build/HDF_Group/HDFView/")[0]
        path = "build/HDF_Group/HDFView/{0}/".format(dir_version)
        hdfview = "{0}/{1}".format(path, "hdfview.sh")

        filter_file(r"\$dir", prefix, hdfview)

        mkdirp(prefix.bin)
        install(hdfview, prefix.bin.hdfview)
        chmod = which("chmod")
        chmod("+x", self.prefix.bin.hdfview)
        install_tree(path, prefix)

    def setup_build_environment(self, env):
        env.set("HDF5LIBS", self.spec["hdf5"].prefix)
        env.set("HDFLIBS", self.spec["hdf"].prefix)
        env.set("ANT_HOME", self.spec["ant"].prefix)
