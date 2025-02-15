# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRjava(RPackage):
    """Low-Level R to Java Interface.

    Low-level interface to Java VM very much like .C/.Call and friends.  Allows
    creation of objects, calling methods and accessing fields."""

    cran = "rJava"

    version("1.0-11", sha256="9ea0ccf5553d86f7de8649a8324766c4f0810f35b7be561640dd87fd37986417")
    version("1.0-6", sha256="e290d0493317a5d6c452793e92baa914e37ef03faef19b2e436329b4ec8658c6")
    version("0.9-13", sha256="5b1688f5044476b34f71d868b222ac5fce3a088f0c2b9e4591c1e48f3d8c75f4")
    version("0.9-11", sha256="c28ae131456a98f4d3498aa8f6eac9d4df48727008dacff1aa561fc883972c69")
    version("0.9-8", sha256="dada5e031414da54eb80b9024d51866c20b92d41d68da65789fe0130bc54bd8a")

    depends_on("r@2.5:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.0-6:")
    depends_on("java@2:")
    depends_on("gmake", type="build")

    # these are not listed as dependencies but are needed
    depends_on("bzip2")
    depends_on("icu4c")
    depends_on("iconv")
    depends_on("pcre2")
    depends_on("xz")
    depends_on("zlib-api")

    def setup_build_environment(self, env):
        spec = self.spec
        env.append_flags("JAVAH", "{0}/javah".format(join_path(spec["java"].prefix.bin)))
