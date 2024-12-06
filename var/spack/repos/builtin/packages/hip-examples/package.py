# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class HipExamples(Package):
    """Examples for HIP"""

    homepage = "https://github.com/ROCm/HIP-Examples/"
    git = "https://github.com/ROCm/HIP-Examples.git"
    url = "https://github.com/ROCm/HIP-Examples/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    version("5.6.1", sha256="c1b5d30e387f869fae21170790ea3d604f7f0dba7771a9c096d9a5c2351dd001")
    version("5.6.0", sha256="b751a0cac938248f7ea0fbeaa9df35688357b54ddd13359e2842a770b7923dfe")
    version("5.5.1", sha256="c8522ef3f0804c85eef7e9efe2671f375b0d7f2100de85f55dcc2401efed6389")
    version("5.5.0", sha256="bea8a4155bbfbdb3bc1f83c22e4bd1214b1b4e1840b58dc7d37704620de5b103")
    version("5.4.3", sha256="053b8b7892e2929e3f90bd978d8bb1c9801e4803eadd7d97fc6692ce60af1d47")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("0001-add-inc-and-lib-paths-to-openmp-helloworld.patch")
    patch("0002-add-fpic-compile-to-add4.patch")

    for ver in ["5.6.1", "5.6.0", "5.5.1", "5.5.0", "5.4.3"]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocm-openmp-extras@" + ver, when="@" + ver)

    def install(self, spec, prefix):
        stage = os.getcwd()
        os.environ["ROCM_OPENMP_EXTRAS_DIR"] = self.spec["rocm-openmp-extras"].prefix
        os.environ["LD_LIBRARY_PATH"] = self.spec["rocm-openmp-extras"].prefix.lib
        for root, dirs, files in os.walk(stage):
            if "Makefile" in files:
                with working_dir(root, create=True):
                    make()
                    # itterate through the files in dir to find the newly built binary
                    for file in os.listdir("."):
                        if file not in files and os.path.isfile(file) and os.access(file, os.X_OK):
                            install(file, join_path(prefix, file))
                            if file == "RecursiveGaussian":
                                install(
                                    "RecursiveGaussian_Input.bmp",
                                    join_path(prefix, "RecursiveGaussian_Input.bmp"),
                                )

    def test_examples(self):
        """
        run all hip example binaries
        """

        os.environ["LD_LIBRARY_PATH"] = self.spec["rocm-openmp-extras"].prefix.lib
        test_dir = self.prefix
        for file_name in os.listdir(test_dir):
            file_path = join_path(test_dir, file_name)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                with test_part(
                    self,
                    "test_example_{0}".format(file_name),
                    purpose="run installed {0}".format(file_name),
                ):
                    exe = which(file_path)
                    exe()
