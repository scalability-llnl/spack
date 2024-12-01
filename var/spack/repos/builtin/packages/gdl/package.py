# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Gdl(CMakePackage):
    """A free and open-source IDL/PV-WAVE compiler.

    GNU Data Language (GDL) is a free/libre/open source incremental compiler
    compatible with IDL and to some extent with PV-WAVE.
    """

    homepage = "https://github.com/gnudatalanguage/gdl"
    url = "https://github.com/gnudatalanguage/gdl/archive/v0.9.9.tar.gz"

    version("0.9.9", sha256="ad5de3fec095a5c58b46338dcc7367d2565c093794ab1bbcf180bba1a712cf14")
    version("0.9.8", sha256="0e22df7314feaf18a76ae39ee57eea2ac8c3633bc095acbc25e1e07277d7c98b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("graphicsmagick", default=False, description="Enable GraphicsMagick")

    variant("hdf4", default=False, description="Enable HDF4")
    variant("hdf5", default=True, description="Enable HDF5")
    variant("openmp", default=True, description="Enable OpenMP")
    variant("proj", default=True, description="Enable LIBPROJ4")
    variant("python", default=False, description="Build the GDL Python module")
    variant("wx", default=False, description="Enable WxWidgets")
    variant("x11", default=False, description="Enable X11")

    extends("python", when="+python")

    depends_on("cmake@3:", type="build")
    depends_on("graphicsmagick", when="+graphicsmagick")
    depends_on("hdf", when="+hdf4")
    depends_on("hdf5", when="+hdf5")
    depends_on("libx11", when="+x11")
    depends_on("plplot+wx", when="+wx@:5.11")
    depends_on("plplot+wx+wxold", when="+wx@5.12:")
    depends_on("plplot~wx", when="~wx")
    # Too many dependencies to test if GDL supports PROJ.6,
    # so restricting to old API
    depends_on("proj@:5", when="+proj")
    depends_on("wxwidgets", when="+wx")

    depends_on("eigen")
    depends_on("fftw")
    depends_on("gsl")
    depends_on("jpeg")
    depends_on("libice")
    depends_on("libsm")
    depends_on("libxinerama")
    depends_on("libxxf86vm")
    depends_on("netcdf-c")
    depends_on("pslib")
    depends_on("readline")
    depends_on("libtirpc", type="link")
    depends_on("libgeotiff", type="link")

    # Building the Python module requires patches currently targetting 0.9.8
    # othwerwise asking for the Python module *only* builds the Python module
    conflicts("+python", when="@:0.9.7,0.9.9:")

    # Allows building gdl as a shared library to in turn allow building
    # both the executable and the Python module
    patch(
        "https://sources.debian.org/data/main/g/gnudatalanguage/0.9.8-7/debian/patches/Create-a-shared-library.patch",
        sha256="bb380394c8ea2602404d8cd18047b93cf00fdb73b83d389f30100dd4b0e1a05c",
        when="@0.9.8",
    )
    patch(
        "Always-build-antlr-as-shared-library.patch",
        sha256="f40c06e8a8f1977780787f58885590affd7e382007cb677d2fb4723aaadd415c",
        when="@0.9.8",
    )

    def cmake_args(self):
        args = []

        # GraphicsMagick covers the same features as ImageMagick and
        # only version 6 of ImageMagick is supported (version 7 is packaged)
        args += ["-DMAGICK=OFF"]

        if self.spec.satisfies("+graphicsmagick"):
            args += ["-DGRAPHICSMAGICK=ON"]
        else:
            args += ["-DGRAPHICSMAGICK=OFF"]

        if self.spec.satisfies("+hdf4"):
            args += ["-DHDF=ON"]
        else:
            args += ["-DHDF=OFF"]

        if self.spec.satisfies("+hdf5"):
            args += ["-DHDF5=ON"]
        else:
            args += ["-DHDF5=OFF"]

        if self.spec.satisfies("+openmp"):
            args += ["-DOPENMP=ON"]
        else:
            args += ["-DOPENMP=OFF"]

        if self.spec.satisfies("+proj"):
            args += ["-DLIBPROJ4=ON", "-DLIBPROJ4DIR={0}".format(self.spec["proj"].prefix)]
        else:
            args += ["-DLIBPROJ4=OFF"]

        if self.spec.satisfies("+python"):
            args += ["-DPYTHON_MODULE=ON"]
        else:
            args += ["-DPYTHON_MODULE=OFF"]

        if self.spec.satisfies("+wx"):
            args += ["-DWXWIDGETS=ON"]
        else:
            args += ["-DWXWIDGETS=OFF"]

        if self.spec.satisfies("+x11"):
            args += ["-DX11=ON"]
        else:
            args += ["-DX11=OFF"]

        return args

    @run_after("install")
    def post_install(self):
        if self.spec.satisfies("+python"):
            # gdl installs the python module into prefix/lib/site-python
            # move it to the standard location
            src = os.path.join(self.spec.prefix.lib, "site-python")
            dst = python_platlib
            if os.path.isdir(src):
                if not os.path.isdir(dst):
                    mkdirp(dst)
                for f in os.listdir(src):
                    os.rename(os.path.join(src, f), os.path.join(dst, f))
