# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygit2(PythonPackage):
    """Pygit2 is a set of Python bindings to the libgit2 shared library,
    libgit2 implements the core of Git.
    """

    homepage = "https://www.pygit2.org/"
    pypi = "pygit2/pygit2-1.12.2.tar.gz"

    version("1.12.1", sha256="56e85d0e66de957d599d1efb2409d39afeefd8f01009bfda0796b42a4b678358")
    version("1.11.1", sha256="793f583fd33620f0ac38376db0f57768ef2922b89b459e75b1ac440377eb64ec")
    version("1.6.0", sha256="7aacea4e57011777f4774421228e5d0ddb9a6ddb87ac4b542346d17ab12a4d62")
    version("1.4.0", sha256="cbeb38ab1df9b5d8896548a11e63aae8a064763ab5f1eabe4475e6b8a78ee1c8")
    version("1.3.0", sha256="0be93f6a8d7cbf0cc79ae2f0afb1993fc055fc0018c27e2bd01ba143e51d4452")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    # https://www.pygit2.org/install.html#version-numbers
    depends_on("libgit2@1.6", when="@1.12")
    depends_on("libgit2@1.5", when="@1.10:1.11")
    depends_on("libgit2@1.4", when="@1.9")
    depends_on("libgit2@1.3", when="@1.7:1.8")
    depends_on("libgit2@1.1", when="@1.4:1.6")
    depends_on("libgit2@1.0", when="@1.2:1.3")
    depends_on("python@3.8:3.11", when="@1.11:1.12.1")
    depends_on("python@:3.10", when="@1.7:1.10")
    depends_on("python@:3.9", when="@1.4:1.6")
    depends_on("python@:3.8", when="@1.0:1.3")
    depends_on("py-cffi@1.4.0:", when="@:1.5", type=("build", "run"))
    depends_on("py-cffi@1.6.0:", when="@1.6:1.7", type=("build", "run"))
    depends_on("py-cffi@1.9.1:", when="@1.8:", type=("build", "run"))
    depends_on("py-cached-property", when="@1.1:1.5", type=("build", "run"))
    depends_on("py-cached-property", when="@1.6: ^python@:3.7", type=("build", "run"))

    def setup_build_environment(self, env):
        spec = self.spec
        # https://www.pygit2.org/install.html
        env.set("LIBGIT2", spec["libgit2"].prefix)
        env.set("LIBGIT2_LIB", spec["libgit2"].prefix.lib)
