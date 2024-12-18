# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyLineProfiler(PythonPackage):
    """Line-by-line profiler."""

    homepage = "https://github.com/pyutils/line_profiler"
    pypi = "line_profiler/line_profiler-2.0.tar.gz"

    license("PSF-2.0")

    version("4.1.2", sha256="aa56578b0ff5a756fe180b3fda7bd67c27bbd478b3d0124612d8cf00e4a21df2")
    version("3.5.1", sha256="77400208bfbd5d4341938a9a3a4fb5194f5af7fc23b2d496c913755f8310e8b8")
    version("2.1.2", sha256="efa66e9e3045aa7cb1dd4bf0106e07dec9f80bc781a993fbaf8162a36c20af5c")
    version("2.0", sha256="739f8ad0e4bcd0cb82e99afc09e00a0351234f6b3f0b1f7f0090a8a2fbbf8381")

    depends_on("c", type="build")  # generated

    # see pyproject.toml
    depends_on("python@2.5:", type=("build", "run"))
    depends_on("python@:3.10", type=("build", "run"), when="@:3")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@68.2.2", type="build", when="@4.1.2:")
    depends_on("py-cython@0.29.24:2", type="build", when="@:4.1.1")
    depends_on("py-cython@3.0.3:", type="build", when="@4.1.2:")
    depends_on("py-ipython@0.13:", type=("build", "run"))
    depends_on("cmake", type="build", when="@3")
    depends_on("ninja", type="build", when="@3")
    depends_on("py-scikit-build@0.9.0:", type="build", when="@3")

    patch("gettimeofday_py39.patch", when="@:2.1.2 ^python@3.9:")

    # See https://github.com/rkern/line_profiler/issues/166
    @run_before("install")
    def fix_cython(self):
        # TODO: Replace the check with a `@when('^python@3.7:')` decorator once
        # https://github.com/spack/spack/issues/12736 is resolved
        if not self.spec.satisfies("^python@3.7:"):
            return
        cython = self.spec["py-cython"].command
        for root, _, files in os.walk("."):
            for fn in files:
                if fn.endswith(".pyx"):
                    cython(os.path.join(root, fn))
