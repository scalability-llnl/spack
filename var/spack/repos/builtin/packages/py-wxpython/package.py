# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWxpython(PythonPackage):
    """Cross platform GUI toolkit for Python."""

    homepage = "https://www.wxpython.org/"
    pypi = "wxPython/wxPython-4.0.6.tar.gz"

    version("4.2.2", sha256="5dbcb0650f67fdc2c5965795a255ffaa3d7b09fb149aa8da2d0d9aa44e38e2ba")
    version("4.1.1", sha256="00e5e3180ac7f2852f342ad341d57c44e7e4326de0b550b9a5c4a8361b6c3528")
    version("4.0.6", sha256="35cc8ae9dd5246e2c9861bb796026bbcb9fb083e4d49650f776622171ecdab37")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("wxwidgets +gui")
    depends_on("wxwidgets@3.2.6 +gui", when="@4.2.2")

    # Needed for the build.py script
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@:75", type="build", when="@:4.1")  # deprecated license-file
    depends_on("py-pathlib2", type="build")

    # Needed at runtime
    depends_on("py-numpy", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))

    def setup_build_environment(self, env):
        # By default wxWdigets is built as well instead of using spack provided version,
        # this tells it to just build the python extensions
        env.set("WXPYTHON_BUILD_ARGS", "build_py --use_syswx")
