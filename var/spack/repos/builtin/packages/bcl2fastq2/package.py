# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

import llnl.util.tty as tty

from spack.package import *
from spack.pkg.builtin.boost import Boost


# This application uses cmake to build, but they wrap it with a
# configure script that performs dark magic.  This package does it
# their way.
class Bcl2fastq2(Package):
    """The bcl2fastq2 Conversion Software converts base
    call (BCL) files from a sequencing run into FASTQ
    files."""

    homepage = "https://support.illumina.com/downloads/bcl2fastq-conversion-software-v2-20.html"

    license("BSD-3-Clause")

    version(
        "2.20.0.422", sha256="8dd3044767d044aa4ce46de0de562b111c44e5b8b7348e04e665eb1b4f101fe3"
    )
    version(
        "2.19.1.403", sha256="cf13580f2c1ebcc3642b4d98a02ad01e41a44e644db7d31730f9767b25521806"
    )

    conflicts("platform=darwin", msg="malloc.h/etc requirements break build on macs")

    depends_on("boost@1.54.0:1.55")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("cmake@2.8.9:", type="build")
    depends_on("libxml2@2.7.8")
    depends_on("libxslt@1.1.26~crypto")
    depends_on("libgcrypt")
    depends_on("zlib-api")

    # Their cmake macros don't set the flag when they find a library
    # that makes them happy.
    patch("cmake-macros.patch")
    # After finding the libxslt bits, cmake still needs to wire in the
    # libexslt bits.
    patch("cxxConfigure-cmake.patch")
    # -msse2 isn't valid for arm
    patch("cxxConfigure-aarch64.patch", when="target=aarch64:")

    root_cmakelists_dir = "src"

    # v2.17.1.14 and v2.18.0.12 were available via HTTP.
    # v2.19.1.403 is only available via ftp.
    # who knows what the future will hold.
    def url_for_version(self, version):
        url = "ftp://webdata2:webdata2@ussd-ftp.illumina.com/downloads/software/bcl2fastq/bcl2fastq2-v{0}-tar.zip"
        if version.string == "2.19.1.403":
            return url.format(version.up_to(3).dotted)
        else:
            return url.format(version.up_to(3).dashed)

    # Illumina tucks the source inside a gzipped tarball inside a zip
    # file.  We let the normal Spack expansion bit unzip the zip file,
    # then follow it with a function untars the tarball after Spack's
    # done it's bit.
    def do_stage(self, mirror_only=False):
        # wrap (decorate) the standard expand_archive step with a
        # helper, then call the real do_stage().
        self.stage.expand_archive = self.unpack_it(self.stage.expand_archive)
        super().do_stage(mirror_only)

    def unpack_it(self, f):
        def wrap():
            f()  # call the original expand_archive()

            # The tarfile should now reside in the well-known source
            # directory (i.e., self.stage.source_path).
            with working_dir(self.stage.path):
                source_subdir = os.path.relpath(self.stage.source_path, self.stage.path)
                files = glob.glob(os.path.join(source_subdir, "bcl2fastq2*.tar.gz"))
                if len(files) == 1:
                    # Rename the tarball so it resides in self.stage.path
                    # alongside the original zip file before unpacking it.
                    tarball = files[0]
                    basename = os.path.basename(tarball)
                    os.rename(tarball, basename)
                    tty.msg("Unpacking bcl2fastq2 tarball")
                    tar = which("tar")
                    tar("-xf", basename)

                    # Rename the unpacked directory to the well-known
                    # source path self.stage.source_path.
                    os.rename("bcl2fastq", source_subdir)
                    tty.msg("Finished unpacking bcl2fastq2 tarball")

                elif self.stage.expanded:
                    # The unpacked files already reside in the "well known"
                    # source directory (i.e., self.stage.source_path).
                    tty.msg("The tarball has already been unpacked.")

        return wrap

    def install(self, spec, prefix):
        bash = which("bash")
        bash(
            "src/configure",
            "--prefix={0}".format(prefix),
            "--with-cmake={0}".format(join_path(spec["cmake"].prefix.bin, "cmake")),
        )
        make()
        make("install")
