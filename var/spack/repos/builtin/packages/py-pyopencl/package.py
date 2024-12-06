# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyopencl(PythonPackage):
    """Python wrapper for OpenCL."""

    homepage = "https://documen.tician.de/pyopencl/"
    pypi = "pyopencl/pyopencl-2020.2.2.tar.gz"

    maintainers("matthiasdiener")

    license("MIT")

    version("2020.2.2", sha256="31fcc79fb6862998e98d91a624c0bd4f0ab4c5d418d199912d4d312c64e437ec")

    depends_on("cxx", type="build")  # generated

    depends_on("ocl-icd", type=("build", "link", "run"))
    depends_on("opencl", type=("build", "link", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-appdirs@1.4.0:", type=("build", "run"))
    depends_on("py-decorator@3.2.0:", type=("build", "run"))
    depends_on("py-mako@0.3.6:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pybind11@2.5.0:", type="build")
    depends_on("py-pytools@2017.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))

    @run_before("install")
    def prepare(self):
        cl_prefix = self.spec["ocl-icd"].prefix
        python(
            "configure.py", "--cl-inc-dir=" + cl_prefix.include, "--cl-lib-dir=" + cl_prefix.lib
        )
