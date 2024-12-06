# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFury(PythonPackage):
    """Free Unified Rendering in Python."""

    homepage = "https://github.com/fury-gl/fury"
    pypi = "fury/fury-0.7.1.tar.gz"

    license("BSD-3-Clause")

    version("0.7.1", sha256="bc7bdbdf1632f317f40c717c2f34a6b8424ce5abda3ebda31a058c0b725a316a")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7.1:", type=("build", "run"))
    depends_on("py-scipy@1.2:", type=("build", "run"))  # from requirements/default.txt
    depends_on("vtk+python@8.1.2:8,9.0.1:", type=("build", "run"))
    depends_on("pil@5.4.1:", type=("build", "run"))

    depends_on("py-coverage", type="test")
    depends_on("py-flake8", type="test")
    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("spack-test", create=True):
            pytest = which("pytest")
            pytest(
                join_path(python_purelib, "fury"),
                # 'Some warning' is not propagated to __warningregistry__ so
                # that the test fails, disable it for now
                # running all tests manually after the package is installed
                # works
                "-k",
                "not test_clear_and_catch_warnings",
            )
