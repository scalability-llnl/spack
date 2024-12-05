# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXdot(PythonPackage):
    """xdot.py is an interactive viewer for graphs written in Graphviz's
    dot language."""

    homepage = "https://github.com/jrfonseca/xdot.py"
    pypi = "xdot/xdot-1.0.tar.gz"
    git = "https://github.com/jrfonseca/xdot.py.git"
    maintainers("lee218llnl")

    version("master", branch="master")
    version("1.2", sha256="3df91e6c671869bd2a6b2a8883fa3476dbe2ba763bd2a7646cf848a9eba71b70")
    version("1.0", sha256="7e067896d729af82f1fd0758e265f129944d469c30f550e3f15dbdb751cc42a1")
    version("0.9", sha256="a33701664ecfefe7c7313a120a587e87334f3a566409bc451538fcde5edd6907")

    # setuptools is required at runtime to avoid:
    # No module named 'pkg_resources'
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-pygobject", type=("build", "run"))
    depends_on("py-pycairo", type=("build", "run"))
    depends_on("pango", type=("build", "run"))
    depends_on("harfbuzz", type=("build", "run"))
    depends_on("atk", type=("build", "run"))
    depends_on("gdk-pixbuf", type=("build", "run"))
    depends_on("gtkplus", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"), when="@1.2:")

    @run_after("install")
    def post_install(self):
        spec = self.spec
        repo_paths = "%s:%s:%s:%s:%s" % (
            join_path(spec["pango"].prefix.lib, "girepository-1.0"),
            join_path(spec["atk"].prefix.lib, "girepository-1.0"),
            join_path(spec["gdk-pixbuf"].prefix.lib, "girepository-1.0"),
            join_path(spec["gtkplus"].prefix.lib, "girepository-1.0"),
            join_path(spec["harfbuzz"].prefix.lib, "girepository-1.0"),
        )
        dst = join_path(python_purelib, "xdot", "__init__.py")
        filter_file(
            "import sys",
            "import sys\nimport os\nos.environ['GI_TYPELIB_PATH']" + " = '%s'" % repo_paths,
            dst,
        )
        # regenerate the byte-compiled __init__.py
        python("-m", "compileall", dst)

    def setup_run_environment(self, env):
        spec = self.spec
        env.prepend_path(
            "GI_TYPELIB_PATH", join_path(spec["harfbuzz"].prefix.lib, "girepository-1.0")
        )
        env.prepend_path(
            "GI_TYPELIB_PATH", join_path(spec["pango"].prefix.lib, "girepository-1.0")
        )
        env.prepend_path("GI_TYPELIB_PATH", join_path(spec["atk"].prefix.lib, "girepository-1.0"))
        env.prepend_path(
            "GI_TYPELIB_PATH", join_path(spec["gdk-pixbuf"].prefix.lib, "girepository-1.0")
        )
        env.prepend_path(
            "GI_TYPELIB_PATH", join_path(spec["gtkplus"].prefix.lib, "girepository-1.0")
        )
