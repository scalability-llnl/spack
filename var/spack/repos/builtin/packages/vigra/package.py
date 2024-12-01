# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Vigra(CMakePackage):
    """VIGRA stands for "Vision with Generic Algorithms". It's an image
    processing and analysis library that puts its main emphasis on
    customizable algorithms and data structures"""

    homepage = "https://ukoethe.github.io/vigra/"
    git = "https://github.com/ukoethe/vigra.git"
    url = (
        "https://github.com/ukoethe/vigra/releases/download/Version-1-11-1/vigra-1.11.1-src.tar.gz"
    )

    license("MIT")

    version("master", branch="master")
    version("1.11.1", sha256="a5564e1083f6af6a885431c1ee718bad77d11f117198b277557f8558fa461aaf")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("png", default=False, description="Include support for PNG images")
    variant("jpeg", default=False, description="Include support for JPEG images")
    variant("tiff", default=False, description="Include support for TIFF images")
    variant("exr", default=False, description="Include support for EXR images")
    variant("hdf5", default=False, description="Include support for HDF5 files")
    variant("fftw", default=False, description="Include support for Fourier Transforms")
    variant("python", default=False, description="Generate Python bindings and doc")
    variant("cxxdoc", default=False, description="Generate C++ documentation")

    depends_on("libtiff", when="+tiff")
    depends_on("libpng", when="+png")
    depends_on("jpeg", when="+jpeg")
    depends_on("hdf5", when="+hdf5")
    depends_on("fftw", when="+fftw")
    depends_on("openexr", when="+exr")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("boost+python+numpy", when="+python")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+python")
    depends_on("py-sphinx", type="build", when="+python")
    depends_on("doxygen", type="build", when="+cxxdoc")
    depends_on("python", type="build", when="+cxxdoc")
    depends_on("py-nose", type=("build", "test"), when="+python")

    extends("python", when="+python")

    def cmake_args(self):
        args = []
        spec = self.spec

        if "+tiff" in spec:
            args.extend(
                [
                    "-DTIFF_LIBRARY={0}".format(spec["libtiff"].libs),
                    "-DTIFF_INCLUDE_DIR={0}".format(spec["libtiff"].prefix.include),
                ]
            )
        if "+hdf5" in spec:
            args.extend(
                [
                    "-DWITH_HDF5=ON",
                    "-DHDF5_CORE_LIBRARY={0}".format(spec["hdf5"].libs.libraries[0]),
                    "-DHDF5_INCLUDE_DIR={0}".format(spec["hdf5"].prefix.include),
                    "-DHDF5_Z_LIBRARY={0}".format(spec["zlib-api"].libs.libraries[0]),
                ]
            )
        else:
            args.append("-DWITH_HDF5=OFF")
        if "+python" in spec:
            py_vers_str = spec["python"].version.up_to(2)
            py_vers_str_nodot = py_vers_str.joined
            boost_python_lib = "{0}/libboost_python{1}.so".format(
                spec["boost"].prefix.lib, py_vers_str_nodot
            )
            args.extend(
                [
                    "-DBoost_DIR={0}".format(spec["boost"].prefix),
                    "-DBoost_INCLUDE_DIR={0}".format(spec["boost"].prefix.include),
                    "-DBoost_PYTHON_LIBRARY={0}".format(boost_python_lib),
                    "-DVIGRANUMPY_INSTALL_DIR={0}".format(python_platlib),
                ]
            )
        if "+fftw" in spec:
            args.extend(
                [
                    "-DFFTW3_LIBRARY={0}".format(spec["fftw"].libs),
                    "-DFFTW3_INCLUDE_DIR={0}".format(spec["fftw"].prefix.include),
                ]
            )
        if "+png" in spec:
            args.extend(
                [
                    "-DPNG_LIBRARY_RELEASE={0}".format(spec["libpng"].libs),
                    "-DPNG_INCLUDE_DIR={0}".format(spec["libpng"].prefix.include),
                ]
            )
        if "+exr" in spec:
            args.append("-DWITH_OPENEXR=ON")
        else:
            args.append("-DWITH_OPENEXR=OFF")
        if "+cxxdoc" in spec:
            args.append("-DDOXYGEN_EXECUTABLE={0}".format(spec["doxygen"].command))
        return args
