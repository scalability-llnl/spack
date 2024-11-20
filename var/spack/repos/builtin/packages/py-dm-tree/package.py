# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyDmTree(PythonPackage):
    """tree is a library for working with nested data structures. In a
    way, tree generalizes the builtin map() function which only
    supports flat sequences, and allows to apply a function to each
    leaf preserving the overall structure."""

    homepage = "https://github.com/deepmind/tree"
    pypi = "dm-tree/dm-tree-0.1.5.tar.gz"

    maintainers("aweits")

    license("Apache-2.0")

    version("0.1.8", sha256="0fcaabbb14e7980377439e7140bd05552739ca5e515ecb3119f234acee4b9430")
    version("0.1.7", sha256="30fec8aca5b92823c0e796a2f33b875b4dccd470b57e91e6c542405c5f77fd2a")
    version(
        "0.1.6",
        sha256="6776404b23b4522c01012ffb314632aba092c9541577004ab153321e87da439a",
        deprecated=True,
    )
    version(
        "0.1.5",
        sha256="a951d2239111dfcc468071bc8ff792c7b1e3192cab5a3c94d33a8b2bda3127fa",
        deprecated=True,
    )

    depends_on("cxx", type="build")

    # Based on PyPI wheel availability
    depends_on("python@:3.12", when="@0.1.8:", type=("build", "run"))
    depends_on("python@:3.10", when="@0.1.6:0.1.7", type=("build", "run"))
    depends_on("python@:3.8", when="@0.1.5", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("cmake@3.12:", when="@0.1.7:", type="build")
    depends_on("py-pybind11@2.10.1:", when="@0.1.8:")
    depends_on("abseil-cpp", when="@0.1.8:")

    patch(
        "https://github.com/google-deepmind/tree/pull/73.patch?full_index=1",
        sha256="77dbd895611d412da99a5afbf312c3c49984ad02bd0e56ad342b2002a87d789c",
        when="@0.1.8",
    )
    conflicts("%gcc@13:", when="@:0.1.7")

    # Historical dependencies
    depends_on("bazel@:5", when="@:0.1.6", type="build")
    depends_on("py-six@1.12.0:", when="@:0.1.6", type=("build", "run"))

    # This is set later
    tmp_path = None

    @run_after("install")
    def clean(self):
        remove_linked_tree(PyDmTree.tmp_path)

    def patch(self):
        PyDmTree.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["TEST_TMPDIR"] = PyDmTree.tmp_path
        env["HOME"] = PyDmTree.tmp_path
        args = [
            # Don't allow user or system .bazelrc to override build settings
            "'--nohome_rc',\n",
            "'--nosystem_rc',\n",
            # Bazel does not work properly on NFS, switch to /tmp
            "'--output_user_root={0}',\n".format(PyDmTree.tmp_path),
            "'build',\n",
            # Spack logs don't handle colored output well
            "'--color=no',\n",
            "'--jobs={0}',\n".format(make_jobs),
            # Enable verbose output for failures
            "'--verbose_failures',\n",
            "'--spawn_strategy=local',\n",
            # bazel uses system PYTHONPATH instead of spack paths
            "'--action_env', 'PYTHONPATH={0}',\n".format(env["PYTHONPATH"]),
        ]
        filter_file("'build',", " ".join(args), "setup.py")
