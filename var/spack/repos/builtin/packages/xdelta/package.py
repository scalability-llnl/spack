# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdelta(AutotoolsPackage):
    """Xdelta version 3 is a C library and command-line tool for delta
    compression using VCDIFF/RFC 3284 streams."""

    homepage = "http://xdelta.org/"
    url = "https://github.com/jmacd/xdelta/archive/v3.1.0.tar.gz"

    version("3.1.0", sha256="7515cf5378fca287a57f4e2fee1094aabc79569cfe60d91e06021a8fd7bae29d")
    version("3.0.11", sha256="28278a4d73127f3d2b00bbde179f8ee1f289ccd3f7f2ac7cd837f6580f90a7b7")
    version("3.0.10", sha256="a3f9c177ec2b91e6d8ec82ee7f0bcbbb2d18fed7d743d7577a990c01235e657d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("go")

    build_directory = "xdelta3"
    configure_directory = "xdelta3"

    def autoreconf(self, spec, prefix):
        with working_dir(self.build_directory):
            bash = which("bash")
            bash(
                "-c",
                "aclocal && autoreconf --install \
                    && libtoolize \
                    && autoconf \
                    && automake --add-missing \
                    && automake",
            )
