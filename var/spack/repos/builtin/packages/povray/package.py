# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# For getting username for defaulting COMPILED_BY
import getpass

# For getting fqdn for defaulting COMPILED_BY
import socket

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Povray(AutotoolsPackage):
    """The Persistence of Vision Raytracer creates three-dimensional,
    photo-realistic images using a rendering technique called ray-tracing. It
    reads in a text file containing information describing the objects and
    lighting in a scene and generates an image of that scene from the view
    point of a camera also described in the text file. Ray-tracing is not a
    fast process by any means, but it produces very high quality images with
    realistic reflections, shading, perspective and other effects.
    """

    homepage = "http://povray.org/download/"
    url = "https://github.com/POV-Ray/povray/archive/v3.7.0.8.tar.gz"
    git = "https://github.com/POV-Ray/povray.git"

    license("AGPL-3.0-or-later")

    version("3.7.0.10", sha256="7bee83d9296b98b7956eb94210cf30aa5c1bbeada8ef6b93bb52228bbc83abff")
    # The following version no longer builds
    version(
        "3.7.0.8",
        sha256="53d11ebd2972fc452af168a00eb83aefb61387662c10784e81b63e44aa575de4",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("boost", default=True, description="Build with boost support")
    variant("debug", default=False, description="Enable compiler debugging mode")
    variant(
        "io-restrictions",
        default=True,
        description="Enable POV-Rays mechanism for control of I/O " "operations",
    )
    variant("jpeg", default=True, description="Build with jpeg support")
    variant("libpng", default=True, description="Build with libpng support")
    variant("libtiff", default=True, description="Build with libtiff support")
    variant("mkl", default=True, description="Build with Intel MKL support")
    variant("openexr", default=True, description="Build with OpenEXR support")
    variant("profile", default=False, description="Enable program execution profiling")
    variant("static", default=False, description="Build static instead shared binaries")
    variant("zlib", default=True, description="Build with zlib support")
    # SDL support is limited to sdl version 1, not sdl2, and spack currently
    # only supports sdl2
    # variant('sdl', default=True,
    #        description='Build with SDL support (for display preview)')
    # X11 support requires SDL, and I believe therefore lacks support for
    # remote displays.  As we do not have SDL support, no X11 support
    # variant('x11', default=True, description='Build with X11 support')

    # Build dependencies
    depends_on("autoconf@2.59:", type="build")
    depends_on("automake@1.9:", type="build")
    depends_on("perl", type="build")
    depends_on("m4", type="build")
    depends_on("boost@1.37:", when="+boost")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+boost")
    depends_on("zlib-api", when="+zlib")
    depends_on("libpng@1.2.5:", when="+libpng")
    depends_on("jpeg", when="+jpeg")
    depends_on("libtiff@3.6.1:", when="+libtiff")
    depends_on("mkl", when="+mkl")
    depends_on("openexr@1.2:", when="+openexr")

    # MKL conflicts
    conflicts("+mkl", when="target=aarch64:", msg="Intel MKL only runs on x86")
    conflicts("+mkl", when="target=ppc64:", msg="Intel MKL only runs on x86")
    conflicts("+mkl", when="target=ppc64le:", msg="Intel MKL only runs on x86")

    # This patch enables prebuild.sh to be invoked from any directory
    # (it immediately cds to the directory containing prebuild.sh)
    # This is better than a broken check that it was called from the
    # containing directory
    patch("fix_prebuild.sh.patch")

    @run_before("autoreconf")
    def run_prebuild_script(self):
        # We need to run <build_dir>/unix/prebuild.sh
        # and it must be run from within the directory containing it
        unix_dir = join_path(self.build_directory, "unix")
        prebuild_path = join_path(unix_dir, "prebuild.sh")
        prebuild_script = which(prebuild_path)
        prebuild_script()

    def configure_args(self):
        extra_args = []

        # POVRay insists upon a COMPILED_BY value being passed to configure
        # We generate a generic using process owner and fqdn of build host.
        fqdn = socket.getfqdn()
        uname = getpass.getuser()
        compiled_by = f"Installed by spack <{uname}@{fqdn}>"
        extra_args.append(f"COMPILED_BY={compiled_by}")

        extra_args.append("--disable-silent-rules")  # Verbose make output
        extra_args += self.enable_or_disable("debug")
        extra_args += self.enable_or_disable("io-restrictions")
        extra_args += self.enable_or_disable("profile")
        extra_args += self.enable_or_disable("static")

        if "+boost" in self.spec:
            extra_args.append(f"--with-boost={self.spec['boost'].prefix}")
        else:
            extra_args.append("--without-boost")

        if "+jpeg" in self.spec:
            extra_args.append(f"--with-libjpeg={self.spec['jpeg'].prefix}")
        else:
            extra_args.append("--without-libjpeg")

        if "+libpng" in self.spec:
            extra_args.append(f"--with-libpng={self.spec['libpng'].prefix}")
        else:
            extra_args.append("--without-libpng")

        if "+libtiff" in self.spec:
            extra_args.append(f"--with-libtiff={self.spec['libtiff'].prefix}")
        else:
            extra_args.append("--without-libtiff")

        if "+mkl" in self.spec:
            extra_args.append(f"--with-libmkl={self.spec['mkl'].prefix}")
        else:
            extra_args.append("--without-libmkl")

        if "+openexr" in self.spec:
            extra_args.append(f"--with-openexr={self.spec['openexr'].prefix}")
        else:
            extra_args.append("--without-openexr")

        # POV-Ray only supports sdl v1, spack only supports sdl2 at this time
        # and X11 support requires sdl
        extra_args.append("--without-libsdl")
        extra_args.append("--without-x")

        return extra_args

    def test_render_sample(self):
        """Render sample file"""
        povs = find(self.prefix.share, "biscuit.pov")[0]
        copy(povs, ".")
        exe = which("povray")
        out = exe("biscuit.pov", output=str.split, error=str.split)
        expected = "POV-Ray finished"
        assert expected in out
