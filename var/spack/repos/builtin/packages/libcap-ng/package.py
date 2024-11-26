# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibcapNg(AutotoolsPackage):
    """Libcap-ng is a library that makes using posix capabilities easier"""

    homepage = "https://github.com/stevegrubb/libcap-ng/"
    url = "https://github.com/stevegrubb/libcap-ng/archive/v0.8.tar.gz"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later")

    version("0.8.3", sha256="e542e9139961f0915ab5878427890cdc7762949fbe216bd0cb4ceedb309bb854")
    version("0.8", sha256="836ea8188ae7c658cdf003e62a241509dd542f3dec5bc40c603f53a5aadaa93f")
    version("0.7.11", sha256="78f32ff282b49b7b91c56d317fb6669df26da332c6fc9462870cec2573352222")
    version("0.7.10", sha256="c3c156a215e5be5430b2f3b8717bbd1afdabe458b6068a8d163e71cefe98fc32")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("attr", type="build")
    depends_on("swig", type="build")
    depends_on("python@2.7:", type=("build", "link", "run"), when="+python")

    variant("python", default=True, description="Enable python")

    extends("python", when="+python")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+python"):
            env.set("PYTHON", python.path)

    def configure_args(self):
        args = []
        spec = self.spec
        if spec.satisfies("+python"):
            if spec.satisfies("^python@3:"):
                args.extend(["--without-python", "--with-python3"])
            else:
                args.extend(["--with-python", "--without-python3"])
        else:
            args.extend(["--without-python", "--without-python3"])
        return args
