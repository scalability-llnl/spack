# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nlopt(CMakePackage):
    """NLopt is a free/open-source library for nonlinear optimization,
    providing a common interface for a number of different free optimization
    routines available online as well as original implementations of various
    other algorithms."""

    homepage = "https://nlopt.readthedocs.io"
    url = "https://github.com/stevengj/nlopt/archive/v2.5.0.tar.gz"
    git = "https://github.com/stevengj/nlopt.git"

    maintainers("cessenat")

    license("LGPL-2.1-or-later")

    version("master", branch="master")

    version("2.7.1", sha256="db88232fa5cef0ff6e39943fc63ab6074208831dc0031cf1545f6ecd31ae2a1a")
    version("2.7.0", sha256="b881cc2a5face5139f1c5a30caf26b7d3cb43d69d5e423c9d78392f99844499f")
    version("2.6.2", sha256="cfa5981736dd60d0109c534984c4e13c615314d3584cf1c392a155bfe1a3b17e")
    version("2.6.1", sha256="66d63a505187fb6f98642703bd0ef006fedcae2f9a6d1efa4f362ea919a02650")
    version("2.6.0", sha256="a13077cdf5f5f1127eaaac0bf1e06744bfe98d8a4a3430a15e0af50a69f451ab")
    version("2.5.0", sha256="c6dd7a5701fff8ad5ebb45a3dc8e757e61d52658de3918e38bab233e7fd3b4ae")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("python", default=True, description="Build python wrappers")
    variant("guile", default=False, description="Enable Guile support")
    variant("octave", default=False, description="Enable GNU Octave support")
    variant("cxx", default=False, description="Build the C++ routines")

    # Note: matlab is licenced - spack does not download automatically
    variant("matlab", default=False, description="Build the Matlab bindings.")

    depends_on("cmake@3.0:", type="build", when="@master")
    depends_on("python", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("swig", when="+python")
    depends_on("guile", when="+guile")
    depends_on("octave", when="+octave")
    depends_on("matlab", when="+matlab")
    extends("python", when="+python")

    def cmake_args(self):
        # Add arguments other than
        # CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        spec = self.spec
        args = []

        # Specify on command line to alter defaults:
        # eg: spack install nlopt@master +guile -octave +cxx

        # On is default
        if "~shared" in spec:
            args.append("-DBUILD_SHARED_LIBS:Bool=OFF")

        # On is default
        if "~octave" in spec:
            args.append("-DNLOPT_OCTAVE:Bool=OFF")

        if "+cxx" in spec:
            args.append("-DNLOPT_CXX:BOOL=ON")

        if "+matlab" in spec:
            args.append("-DMatlab_ROOT_DIR=%s" % spec["matlab"].command.path)

        return args
