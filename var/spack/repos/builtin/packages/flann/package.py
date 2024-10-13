# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Flann(CMakePackage):
    """FLANN is a library for performing fast approximate nearest neighbor
    searches in high dimensional spaces. It contains a collection of
    algorithms we found to work best for nearest neighbor search and a system
    for automatically choosing the best algorithm and optimum parameters
    depending on the dataset.

    FLANN is written in C++ and contains bindings for the following languages:
    C, MATLAB and Python.
    """

    homepage = "https://github.com/mariusmuja/flann"
    url = "https://github.com/mariusmuja/flann/archive/1.9.1.tar.gz"

    license("BSD-3-Clause")

    version("1.9.2", sha256="e26829bb0017f317d9cc45ab83ddcb8b16d75ada1ae07157006c1e7d601c8824")
    version("1.9.1", sha256="b23b5f4e71139faa3bcb39e6bbcc76967fbaf308c4ee9d4f5bfbeceaa76cc5d3")
    version("1.8.5", sha256="59a9925dac0705b281496ae52b5dfd79d6b69316d37015e3d3b38c859bac4f2f")
    version("1.8.4", sha256="ed5843113150b3d6bc4c325fecb51337838a9fc09ad64bdb6aea79d6e610ee13")
    version("1.8.1", sha256="82ff80709ca25365bca3367e87ffb4e0395fab068487314d02271bc3034591c1")
    version("1.8.0", sha256="8a3eef79512870dec20b3a3e481e5e5e6da00d524b810a22ee186f13732f0fa1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version > Version("1.8.1"):
            return "https://github.com/mariusmuja/flann/archive/{0}.tar.gz".format(version)
        else:
            return "https://github.com/mariusmuja/flann/archive/{0}-src.tar.gz".format(version)

    # Options available in the CMakeLists.txt
    # Language bindings
    variant("python", default=False, description="Build the Python bindings. " "Module: pyflann.")
    extends("python", when="+python")
    variant("matlab", default=False, description="Build the Matlab bindings.")
    # default to true for C because it's a C++ library, nothing extra needed
    variant("c", default=True, description="Build the C bindings.")

    # Must build C bindings for Python / Matlab
    conflicts("+python", when="~c")
    conflicts("+matlab", when="~c")

    # Additional options
    variant("cuda", default=False, description="Build the CUDA library.")
    variant("examples", default=False, description="Build the examples.")
    variant("doc", default=False, description="Build the documentation.")
    variant("openmp", default=True, description="Use OpenMP multi-threading.")
    # mpi and hdf5 are the bread and butter of this library, use 'em
    variant("mpi", default=True, description="Use MPI.")
    variant("hdf5", default=True, description="Enable HDF5 support.")

    # Dependencies
    extends("python", when="+python")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("matlab", when="+matlab", type=("build", "run"))
    depends_on("cuda", when="+cuda")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5", when="+hdf5")
    depends_on("lz4", when="@1.9.2:")
    # HDF5_IS_PARALLEL actually comes from hdf5+mpi
    # https://github.com/mariusmuja/flann/blob/06a49513138009d19a1f4e0ace67fbff13270c69/CMakeLists.txt#L108-L112
    depends_on(
        "boost+mpi+system+serialization+thread+regex+graph+chrono+exception", when="+mpi ^hdf5+mpi"
    )

    # Doc deps
    depends_on("texlive", when="+doc")

    # Example uses hdf5.
    depends_on("hdf5", when="+examples")

    depends_on("hdf5", type="test")
    depends_on("googletest", type="test")

    # See: https://github.com/mariusmuja/flann/issues/369
    patch("linux-gcc-cmakev3.11-plus.patch", when="@:1.9.1%gcc^cmake@3.11:")

    def patch(self):
        # Fix up the python setup.py call inside the install(CODE
        filter_file(
            "setup.py install",
            'setup.py --no-user-cfg install --prefix=\\"{0}\\"'.format(self.prefix),
            "src/python/CMakeLists.txt",
        )
        # Fix the install location so that spack activate works
        if self.spec.satisfies("+python"):
            filter_file("share/flann/python", python_platlib, "src/python/CMakeLists.txt")
        # Hack. Don't install setup.py
        filter_file("install( FILES", "# install( FILES", "src/python/CMakeLists.txt", string=True)

    def cmake_args(self):
        spec = self.spec
        args = []

        # Language bindings. Many default to true in CMakeLists, bypass all
        c_bind = "ON" if "+c" in spec else "OFF"
        args.append("-DBUILD_C_BINDINGS:BOOL={0}".format(c_bind))

        py_bind = "ON" if "+python" in spec else "OFF"
        args.append("-DBUILD_PYTHON_BINDINGS:BOOL={0}".format(py_bind))

        mat_bind = "ON" if "+matlab" in spec else "OFF"
        args.append("-DBUILD_MATLAB_BINDINGS:BOOL={0}".format(mat_bind))

        # Extra options
        cuda_lib = "ON" if "+cuda" in spec else "OFF"
        args.append("-DBUILD_CUDA_LIB:BOOL={0}".format(cuda_lib))

        examples = "ON" if "+examples" in spec else "OFF"
        args.append("-DBUILD_EXAMPLES:BOOL={0}".format(examples))

        use_openmp = "ON" if "+openmp" in spec else "OFF"
        args.append("-DUSE_OPENMP:BOOL={0}".format(use_openmp))

        use_mpi = "ON" if "+mpi" in spec else "OFF"
        args.append("-DUSE_MPI:BOOL={0}".format(use_mpi))

        return args
