# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEccodes(PythonPackage):
    """Python interface to the ecCodes GRIB and BUFR decoder/encoder."""

    homepage = "https://github.com/ecmwf/eccodes-python"
    pypi = "eccodes/eccodes-1.3.2.tar.gz"

    license("Apache-2.0")

    version("1.5.0", sha256="e70c8f159140c343c215fd608ddf533be652ff05ad2ff17243c7b66cf92127fa")
    version("1.4.2", sha256="63fa80a1d1b445904f486bc396a6a6605df029f4e215acc28ceb1a1ff5eb664f")
    version("1.3.2", sha256="f282adfdc1bc658356163c9cef1857d4b2bae99399660d3d4fcb145a52d3b2a6")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-attrs", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-findlibs", type=("build", "run"))
    depends_on("eccodes@2.21.0:+shared", type="run")

    def setup_build_environment(self, env):
        eccodes_spec = self.spec["eccodes:c,shared"]
        # ECCODES_HOME has the highest precedence when searching for the library with py-findlibs:
        env.set("ECCODES_HOME", eccodes_spec.prefix)
        # but not if ecmwflibs (https://pypi.org/project/ecmwflibs/) is in the PYTHONPATH:
        env.set("ECMWFLIBS_ECCODES", eccodes_spec.libs.files[0])

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    def test_selfcheck(self):
        """checking system setup"""
        python("-m", "eccodes", "selfcheck")
