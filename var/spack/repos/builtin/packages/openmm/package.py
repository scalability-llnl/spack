# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openmm(CMakePackage, CudaPackage):
    """A high performance toolkit for molecular simulation. Use it as
    a library, or as an application. We include extensive language
    bindings for Python, C, C++, and even Fortran. The code is open
    source and actively maintained on Github, licensed under MIT and
    LGPL. Part of the Omnia suite of tools for predictive biomolecular
    simulation."""

    homepage = "https://openmm.org/"
    url = "https://github.com/openmm/openmm/archive/7.4.1.tar.gz"

    version("8.1.1", sha256="347ad9f04dd88a673f7871127d9f23a75caf2c1a460a3f21f3328a24dc6547d0")
    version("8.0.0", sha256="dc63d7b47c8bb7b169c409cfd63d909ed0ce1ae114d37c627bf7a4231acf488e")
    version("7.7.0", sha256="51970779b8dc639ea192e9c61c67f70189aa294575acb915e14be1670a586c25")
    version("7.6.0", sha256="5a99c491ded9ba83ecc3fb1d8d22fca550f45da92e14f64f25378fda0048a89d")
    version("7.5.1", sha256="c88d6946468a2bde2619acb834f57b859b5e114a93093cf562165612e10f4ff7")
    version("7.5.0", sha256="516748b4f1ae936c4d70cc6401174fc9384244c65cd3aef27bc2c53eac6d6de5")
    version("7.4.1", sha256="e8102b68133e6dcf7fcf29bc76a11ea54f30af71d8a7705aec0aee957ebe3a6d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    install_targets = ["install", "PythonInstall"]

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("cmake@3.17:", type="build", when="@7.5.1:")
    depends_on("cmake@3.1:", type="build")
    # https://github.com/openmm/openmm/issues/3317
    depends_on("doxygen@:1.9.1", type="build", when="@:7.6.0")
    depends_on("doxygen", type="build", when="@7.7:")
    depends_on("swig", type="build")
    depends_on("fftw", when="@:7")
    depends_on("py-cython", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("cuda", when="+cuda", type=("build", "link", "run"))
    extends("python")

    # Backport <https://github.com/openmm/openmm/pull/3154> to
    # `openmm@7.5.1+cuda`, which is the version currently required by
    # `py-alphafold`.
    patch(
        "https://github.com/openmm/openmm/pull/3154.patch?full_index=1",
        sha256="90bc01b34cf998e90220669b3ed55cd3c42000ad364234033aac631ed754e9bd",
        when="@7.5.1+cuda",
    )

    def patch(self):
        install_string = f'set(PYTHON_SETUP_COMMAND "install --prefix={self.prefix}")'

        filter_file(
            r"set\(PYTHON_SETUP_COMMAND \"install.*",
            install_string,
            "wrappers/python/CMakeLists.txt",
        )

    def setup_build_environment(self, env):
        spec = self.spec
        if "+cuda" in spec:
            env.set("OPENMM_CUDA_COMPILER", self.spec["cuda"].prefix.bin.nvcc)
            env.set("CUDA_HOST_COMPILER", self.compiler.cxx)

    def setup_run_environment(self, env):
        spec = self.spec
        if "+cuda" in spec:
            env.set("OPENMM_CUDA_COMPILER", self.spec["cuda"].prefix.bin.nvcc)
            env.set("CUDA_HOST_COMPILER", self.compiler.cxx)

    def setup_dependent_run_environment(self, env, dependent_spec):
        spec = self.spec
        if "+cuda" in spec:
            env.set("OPENMM_CUDA_COMPILER", self.spec["cuda"].prefix.bin.nvcc)
            env.set("CUDA_HOST_COMPILER", self.compiler.cxx)

    def setup_dependent_build_environment(self, env, dependent_spec):
        spec = self.spec
        if "+cuda" in spec:
            env.set("OPENMM_CUDA_COMPILER", self.spec["cuda"].prefix.bin.nvcc)
            env.set("CUDA_HOST_COMPILER", self.compiler.cxx)
