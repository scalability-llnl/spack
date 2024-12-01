# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMccabe(PythonPackage):
    """Ned's script to check McCabe complexity."""

    homepage = "https://github.com/PyCQA/mccabe"
    pypi = "mccabe/mccabe-0.7.0.tar.gz"

    license("MIT")

    version("0.7.0", sha256="348e0240c33b60bbdf4e523192ef919f28cb2c3d7d5c7794f74009290f236325")
    version("0.6.1", sha256="dd8d182285a0fe56bace7f45b5e7d1a6ebcbf524e8f3bd87eb0f125271b8831f")
    version("0.6.0", sha256="de9bbfe5b771e4c11b1521f3e338fe265a12296b59302f43a3bbf3e02d4b98b1")
    version("0.5.3", sha256="16293af41e7242031afd73896fef6458f4cad38201d21e28f344fff50ae1c25e")
    version("0.5.2", sha256="3473f06c8b757bbb5cdf295099bf64032e5f7d6fe0ec2f97ee9b23cb0a435aff")
    version("0.5.1", sha256="8a30b9cb533b2bde819e7143bd56efc8b52e2fb9ed5ab0983cfd52ca596f88b2")
    version("0.5.0", sha256="379358498f58f69157b53f59f46aefda0e9a3eb81365238f69fbedf7014e21ab")
    version("0.4.0", sha256="9a2b12ebd876e77c72e41ebf401cc2e7c5b566649d50105ca49822688642207b")
    version("0.3.1", sha256="5f7ea6fb3aa9afe146d07fd6d5cedf788747d8b0c29e44732453c2b2db1e3d16")
    version("0.3", sha256="3d8ca9bf65c5014f469180544d1dd5bb5b9df709aad6304f9c2e4370ae0a7b7c")
    version("0.2.1", sha256="5a2a170e47de5593a6abfae1e9542bd2c3924ac62bbe4e6ed96c953c0352243a")
    version("0.2", sha256="e0210235022d05d11b3c4c86e2cb65d5b307ab46ac88882d20ff998fd2ef0ad4")

    depends_on("python@3.6:", when="@0.7:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    @when("@:0.6")
    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", "setup.py", string=True)
