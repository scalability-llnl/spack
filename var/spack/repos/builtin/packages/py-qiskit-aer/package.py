# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQiskitAer(PythonPackage, CudaPackage):
    """Aer is a high performance simulator for quantum circuits that
    includes noise models"""

    homepage = "https://github.com/Qiskit/qiskit-aer"
    pypi = "qiskit-aer/qiskit-aer-0.9.1.tar.gz"

    license("Apache-2.0")

    version("0.11.1", sha256="ff136a086d0473346e5f5309ae34cc78b103dcd8a898344c6e5f86de91af41a1")
    version("0.9.1", sha256="3bf5f615aaae7cc5f816c39a4e9108aabaed0cc894fb6f841e48ffd56574e7eb")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"), when="@0.9.1")
    depends_on("python@3.7:", type=("build", "run"), when="@0.11.1")
    depends_on("py-setuptools@40.1.0:", type="build")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")
    depends_on("py-numpy@1.16.3:", type=("build", "run"))
    depends_on("py-pybind11@2.6:", type="build")
    depends_on("py-qiskit-terra@0.17.0:", type=("build", "run"))
    depends_on("py-qiskit-terra@0.21.0:", type=("build", "run"), when="@0.11.1")
    depends_on("py-scipy@1.0:", type=("build", "run"))
    depends_on("py-scikit-build@0.11.0:", type="build")
    depends_on("cmake@:3.16,3.18:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("nlohmann-json@3.1.1:")
    depends_on("spdlog@1.5.0:")
    depends_on("muparserx@4.0.8:")
    depends_on("blas")
    depends_on("cuda@10.1:", when="+cuda")

    variant("mpi", default=True, description="Enable MPI support")
    variant("gdr", default=True, description="Enable GDR support")

    def setup_build_environment(self, env):
        env.set("DISABLE_CONAN", "ON")
        env.set("DISABLE_DEPENDENCY_INSTALL", "1")
        env.set("CUDAHOSTCXX", spack_cxx)

    def install_options(self, spec, prefix):
        args = []
        args.append("-DDISABLE_CONAN=ON")
        if "~gdr" in self.spec:
            args.append("-DAER_DISABLE_GDR=True")
        else:
            args.append("-DAER_DISABLE_GDR=False")
        if "+mpi" in self.spec:
            args.append("-DAER_MPI=True")
        else:
            args.append("-DAER_MPI=False")
        if "+cuda" in self.spec:
            args.append("-DAER_THRUST_BACKEND=CUDA")
            cuda_archs = spec.variants["cuda_arch"].value
            if "none" not in cuda_archs:
                args.append("-DCUDA_NVCC_FLAGS={0}".format(" ".join(self.cuda_flags(cuda_archs))))
        return args
