# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lrzip(Package):
    """A compression utility that excels at compressing large files
    (usually > 10-50 MB). Larger files and/or more free RAM means that the
    utility will be able to more effectively compress your files (ie: faster /
    smaller size), especially if the filesize(s) exceed 100 MB. You can either
    choose to optimise for speed (fast compression / decompression) or size,
    but not both."""

    homepage = "http://lrzip.kolivas.org"
    url = "https://github.com/ckolivas/lrzip/archive/v0.630.tar.gz"
    git = "https://github.com/ckolivas/lrzip.git"

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("0.651", sha256="f4c84de778a059123040681fd47c17565fcc4fec0ccc68fcf32d97fad16cd892")
    version("0.630", sha256="7b9bf6415fb2294a8e83a5a1c6a8d7da17a19f4730567c8fa16e3016d79250a6")
    version("0.621", sha256="4bf93c1df076b6e6a57f32c0c4b7790b4d25d724c259394e1d32b680c0657121")
    version("0.616", sha256="6ef50bfec15d7585e5b085067c9fe91a87246ccd14a3165acd08b147bba26a2e")
    version("0.615", sha256="45bc3e09a9c467c9331499e4e7919ea97d0824d24a1f2c3ec9548bb2b9d14898")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # depends_on('coreutils')
    depends_on("lzo")
    depends_on("zlib-api")
    depends_on("bzip2")

    def install(self, spec, prefix):
        set_executable("./autogen.sh")
        autogen = Executable("./autogen.sh")

        configure_args = ["--prefix={0}".format(prefix), "--disable-dependency-tracking"]
        autogen(*configure_args)

        make()
        make("install")
