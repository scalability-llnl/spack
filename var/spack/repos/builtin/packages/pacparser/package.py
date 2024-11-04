# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pacparser(MakefilePackage):
    """pacparser is a library to parse proxy auto-config (PAC) files."""

    homepage = "https://pacparser.github.io/"
    url = "https://github.com/manugarg/pacparser/archive/refs/tags/v1.4.5.tar.gz"
    git = "https://github.com/manugarg/pacparser.git"

    license("LGPL-3.0-or-later")

    version("1.4.5", sha256="fac205f41d000e245519244dc3e730e649a0ac1c61b5f2d1d0660056e1680b2d")
    version("1.4.0", sha256="2e66c5fe635cd5dcb9bccca4aced925eca712632b81bada3b63682159c0f910e")
    version("1.3.9", commit="4bbfb15c96ea0b2aede2f7371e59f66e15722d41")
    version("1.3.8", sha256="4e2872de565b2b64ffc81ba503e0eba35b3f7ef4a023ddd4a328c7b9d2cac266")
    version(
        "1.3.7",
        sha256="eb48ec2fc202d12a4b882133048c7590329849f32c2285bc4dbe418f29aad249",
        url="https://github.com/manugarg/pacparser/releases/download/1.3.7/pacparser-1.3.7.tar.gz",
    )

    depends_on("c", type="build")  # generated

    depends_on("python", when="+python")
    depends_on("py-setuptools", when="+python", type=("build", "run"))

    extends("python", when="+python")

    variant("python", default=False, description="Build and install python bindings")

    def url_for_version(self, version):
        if version <= Version("1.4.0"):
            return f"https://github.com/manugarg/pacparser/releases/download/v{version}/pacparser-v{version}.tar.gz"
        else:
            return f"https://github.com/manugarg/pacparser/archive/refs/tags/v{version}.tar.gz"

    def build(self, spec, prefix):
        make('CC="%s"' % self.compiler.cc, 'CXX="%s"' % self.compiler.cxx, "-C", "src")
        if "+python" in spec:
            make(
                'CC="%s"' % self.compiler.cc, 'CXX="%s"' % self.compiler.cxx, "-C", "src", "pymod"
            )

    def install(self, spec, prefix):
        make("-C", "src", "install", "PREFIX=" + self.prefix)
        if "+python" in spec:
            make(
                "-C",
                "src",
                "install-pymod",
                "PREFIX=" + self.prefix,
                "EXTRA_ARGS=--prefix={0}".format(prefix),
            )
