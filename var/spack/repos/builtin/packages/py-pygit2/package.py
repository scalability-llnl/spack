# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygit2(PythonPackage):
    """Pygit2 is a set of Python bindings to the libgit2 shared library,
    libgit2 implements the core of Git.
    """

    homepage = "https://www.pygit2.org/"
    pypi = "pygit2/pygit2-1.16.0.tar.gz"

    version("1.16.0", sha256="7b29a6796baa15fc89d443ac8d51775411d9b1e5b06dc40d458c56c8576b48a2")
    version("1.15.1", sha256="e1fe8b85053d9713043c81eccc74132f9e5b603f209e80733d7955eafd22eb9d")
    version("1.15.0", sha256="a635525ffc74128669de2f63460a94c9d5609634a4875c0aafce510fdeec17ac")
    version("1.14.1", sha256="ec5958571b82a6351785ca645e5394c31ae45eec5384b2fa9c4e05dde3597ad6")
    version("1.14.0", sha256="f529ed9660edbf9b625ccae7e51098ef73662e61496609009772d4627a826aa8")
    version("1.13.3", sha256="0257c626011e4afb99bdb20875443f706f84201d4c92637f02215b98eac13ded")
    version("1.13.2", sha256="75c7eb86b47c70f6f1434bcf3b5eb41f4e8006a15cee6bef606651b97d23788c")
    version("1.13.1", sha256="d8e6d540aad9ded1cf2c6bda31ba48b1e20c18525807dbd837317bef4dccb994")
    version("1.13.0", sha256="6dde37436fab14264ad3d6cbc5aae3fd555eb9a9680a7bfdd6e564cd77b5e2b8")
    version("1.12.2", sha256="56e85d0e66de957d599d1efb2409d39afeefd8f01009bfda0796b42a4b678358")
    version("1.12.1", sha256="8218922abedc88a65d5092308d533ca4c4ed634aec86a3493d3bdf1a25aeeff3")
    version("1.12.0", sha256="e9440d08665e35278989939590a53f37a938eada4f9446844930aa2ee30d73be")
    version("1.11.1", sha256="793f583fd33620f0ac38376db0f57768ef2922b89b459e75b1ac440377eb64ec")
    version("1.6.0", sha256="7aacea4e57011777f4774421228e5d0ddb9a6ddb87ac4b542346d17ab12a4d62")
    version("1.4.0", sha256="cbeb38ab1df9b5d8896548a11e63aae8a064763ab5f1eabe4475e6b8a78ee1c8")
    version(
        "1.3.0",
        sha256="0be93f6a8d7cbf0cc79ae2f0afb1993fc055fc0018c27e2bd01ba143e51d4452",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    # https://www.pygit2.org/install.html#version-numbers
    depends_on("libgit2@1.8", when="@1.15:")
    depends_on("libgit2@1.7", when="@1.13:1.14")
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
