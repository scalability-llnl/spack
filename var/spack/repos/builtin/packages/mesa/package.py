# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

import spack.build_systems.meson
from spack.package import *


class Mesa(MesonPackage):
    """Mesa is an open-source implementation of the OpenGL specification
    - a system for rendering interactive 3D graphics."""

    homepage = "https://www.mesa3d.org"
    maintainers("v-dobrev")

    git = "https://gitlab.freedesktop.org/mesa/mesa.git"
    url = "https://archive.mesa3d.org/mesa-20.2.1.tar.xz"

    license("MIT AND SGI-B-2.0 AND BSL-1.0")

    version("main", branch="main")
    version(
        "23.3.6",
        sha256="cd3d6c60121dea73abbae99d399dc2facaecde1a8c6bd647e6d85410ff4b577b",
        preferred=True,
    )
    version("23.2.1", sha256="64de0616fc2d801f929ab1ac2a4f16b3e2783c4309a724c8a259b20df8bbc1cc")
    version("23.1.9", sha256="295ba27c28146ed09214e8ce79afa1659edf9d142decc3c91f804552d64f7510")
    version("23.0.3", sha256="386362a5d80df3b096636b67f340e1ce67b705b44767d5bdd11d2ed1037192d5")
    version("23.0.2", sha256="1b7d3399fc6f16f030361f925d33ebc7600cbf98094582f54775b6a1180529e7")
    version("22.3.2", sha256="c15df758a8795f53e57f2a228eb4593c22b16dffd9b38f83901f76cd9533140b")
    version("22.2.5", sha256="850f063146f8ebb262aec04f666c2c1e5623f2a1987dda24e4361b17b912c73b")
    version("22.1.6", sha256="22ced061eb9adab8ea35368246c1995c09723f3f71653cd5050c5cec376e671a")
    version("22.1.2", sha256="0971226b4a6a3d10cfc255736b33e4017e18c14c9db1e53863ac1f8ae0deb9ea")
    version("22.0.5", sha256="5ee2dc06eff19e19b2867f12eb0db0905c9691c07974f6253f2f1443df4c7a35")
    version("22.0.2", sha256="df4fa560dcce6680133067cd15b0505fc424ca703244ce9ab247c74d2fab6885")
    version("21.3.8", sha256="e70d273bdc53a4e931871bb5550ba3900e6a3deab2fff64184107c33e92d9da7")
    version("21.3.7", sha256="b4fa9db7aa61bf209ef0b40bef83080999d86ad98df8b8b4fada7c128a1efc3d")
    version("21.3.1", sha256="2b0dc2540cb192525741d00f706dbc4586349185dafc65729c7fda0800cc474d")
    version("21.2.6", sha256="1e7e22d93c6e8859fa044b1121119d26b2e67e4184b92ebb81c66497dc80c954")
    version("21.2.5", sha256="8e49585fb760d973723dab6435d0c86f7849b8305b1e6d99f475138d896bacbb")
    version("21.2.4", sha256="fe6ede82d1ac02339da3c2ec1820a379641902fd351a52cc01153f76eff85b44")
    version("21.2.3", sha256="7245284a159d2484770e1835a673e79e4322a9ddf43b17859668244946db7174")
    version("21.2.1", sha256="2c65e6710b419b67456a48beefd0be827b32db416772e0e363d5f7d54dc01787")
    version("21.0.3", sha256="565c6f4bd2d5747b919454fc1d439963024fc78ca56fd05158c3b2cde2f6912b")
    version("21.0.0", sha256="e6204e98e6a8d77cf9dc5d34f99dd8e3ef7144f3601c808ca0dd26ba522e0d84")
    version("20.3.4", sha256="dc21a987ec1ff45b278fe4b1419b1719f1968debbb80221480e44180849b4084")
    version("20.2.1", sha256="d1a46d9a3f291bc0e0374600bdcb59844fa3eafaa50398e472a36fc65fd0244a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("meson@0.52:", type="build")

    depends_on("pkgconfig", type="build")
    depends_on("bison", type="build")
    depends_on("cmake", type="build")
    depends_on("flex", type="build")
    depends_on("gettext", type="build")
    # Upperbound on 3.11 because distutils is used for checking py-mako
    depends_on("python@3:3.11", type="build")
    depends_on("py-mako@0.8.0:", type="build")
    depends_on("unwind")
    depends_on("expat")
    depends_on("zlib-api")
    depends_on("libxml2")

    # Internal options
    variant("llvm", default=True, description="Enable LLVM.")

    # when clauses:
    #   +llvm - swr requires llvm
    #   buildtype=release - swr has known assert failures in debug that can be ignored
    #   @:21  - swr was removed in 22.0
    variant(
        "swr",
        values=spack.variant.DisjointSetsOfValues(
            ("none",), ("auto",), ("avx", "avx2", "knl", "skx")
        )
        .with_non_feature_values("auto")
        .with_non_feature_values("none")
        .with_default("auto"),
        when="+llvm buildtype=release @:21",
        description="Enable the SWR driver.",
    )

    # Front ends
    variant("osmesa", default=True, description="Enable the OSMesa frontend.", when="+opengl")

    is_linux = sys.platform.startswith("linux")
    variant("glx", default=is_linux, description="Enable the GLX frontend.", when="+opengl")

    # TODO: effectively deal with EGL.  The implications of this have not been
    # worked through yet
    # variant('egl', default=False, description="Enable the EGL frontend.")

    # TODO: Effectively deal with hardware drivers
    # The implication of this is enabling DRI, among other things, and
    # needing to check which llvm targets were built (ptx or amdgpu, etc.)

    # Back ends
    variant("opengl", default=True, description="Enable full OpenGL support.")
    variant("opengles", default=False, description="Enable OpenGL ES support.")

    # Provides
    provides("libglx", when="+glx")
    # provides('egl@1.5', when='+egl')

    # Variant dependencies
    with when("+llvm"):
        depends_on("libllvm@6:")
        depends_on("libllvm@:11", when="@:20")
        depends_on("libllvm@:12", when="@:21")
        depends_on("libllvm@:17", when="@:23")

    with when("+glx"):
        depends_on("libx11")
        depends_on("libxcb")
        depends_on("libxext")
        depends_on("libxt")
        depends_on("xrandr")
        depends_on("glproto@1.4.14:")

    # version specific issue
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=96130
    conflicts("%gcc@10.1.0", msg="GCC 10.1.0 has a bug")

    # Require at least 1 front-end
    # TODO: Add egl to this conflict once made available
    conflicts("~osmesa ~glx")

    # Require at least 1 back-end
    # TODO: Add vulkan to this conflict once made available
    conflicts("~opengl ~opengles")

    # OpenGL ES requires OpenGL
    conflicts("~opengl +opengles")

    # requires native to be added to llvm_modules when using gallium swrast
    patch(
        "https://cgit.freedesktop.org/mesa/mesa/patch/meson.build?id=054dd668a69acc70d47c73abe4646e96a1f23577",
        sha256="36096a178070e40217945e12d542dfe80016cb897284a01114d616656c577d73",
        when="@21.0.0:21.0.3",
    )

    # llvm::Module::setOverrideStackAlignment was added in LLVM 13.0.0, but forks based
    # on development versions of LLVM 13 may or may not have it. Use SFINAE to detect
    # the existence of the function and call it only if it is available.
    patch("handle_missing_set_override_stack_alignment.patch", when="@21.2.3:22.3")

    # ROCm 5.3.0 is providing llvm15. Gallivm coroutine is disabled in mesa upstream version
    # for llvm-15. Until mesa release is available with this changes below patch is required
    # in order to move on with ROCm 5.3.0 and ROCm 5.4.0.
    # The revised patch was part of https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/17518/diffs.

    patch("0001-disable-gallivm-coroutine-for-libllvm15.patch", when="@22.1.2:22.3 ^libllvm@15")

    # Explicitly use the llvm-config tool
    def patch(self):
        filter_file(r"_llvm_method = 'auto'", "_llvm_method = 'config-tool'", "meson.build")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%intel"):
            if name == "cflags":
                flags.append("-std=c99")
        return super().flag_handler(name, flags)

    @property
    def libglx_headers(self):
        return find_headers("GL/glx", root=self.spec.prefix.include, recursive=False)

    @property
    def libglx_libs(self):
        return find_libraries("libGL", root=self.spec.prefix, recursive=True)

    @property
    def libosmesa_headers(self):
        return find_headers("GL/osmesa", root=self.spec.prefix.include, recursive=False)

    @property
    def libosmesa_libs(self):
        if "platform=windows" in self.spec:
            lib_name = "osmesa"
        else:
            lib_name = "libOSMesa"
        return find_libraries(lib_name, root=self.spec.prefix, recursive=True)


class MesonBuilder(spack.build_systems.meson.MesonBuilder):
    def meson_args(self):
        spec = self.spec
        args = [
            "-Dvulkan-drivers=",
            "-Dgallium-vdpau=disabled",
            "-Dgallium-omx=disabled",
            "-Dgallium-va=disabled",
            "-Dgallium-xa=disabled",
            "-Dgallium-nine=false",
            "-Dgallium-opencl=disabled",
            "-Dbuild-tests=false",
            "-Dglvnd=false",
        ]
        # gallium-xvmc was removed in @main and @2.23:
        if self.spec.satisfies("@:22.2"):
            args.append("-Dgallium-xvmc=disabled")

        args_platforms = []
        args_gallium_drivers = ["swrast"]
        args_dri_drivers = []

        opt_enable = lambda c, o: "-D%s=%sabled" % (o, "en" if c else "dis")
        opt_bool = lambda c, o: "-D%s=%s" % (o, str(c).lower())
        if spec.target.family == "arm" or spec.target.family == "aarch64":
            args.append("-Dlibunwind=disabled")

        num_frontends = 0

        if spec.satisfies("@:20.3"):
            osmesa_enable, osmesa_disable = ("gallium", "none")
        else:
            osmesa_enable, osmesa_disable = ("true", "false")

        if "+osmesa" in spec:
            num_frontends += 1
            args.append("-Dosmesa={0}".format(osmesa_enable))
        else:
            args.append("-Dosmesa={0}".format(osmesa_disable))

        if "+glx" in spec:
            num_frontends += 1
            if "+egl" in spec:
                args.append("-Dglx=dri")
            else:
                if spec.satisfies("@22:"):
                    args.append("-Dglx=xlib")
                else:
                    args.append("-Dglx=gallium-xlib")
            args_platforms.append("x11")
        else:
            args.append("-Dglx=disabled")

        if "+egl" in spec:
            num_frontends += 1
            args.extend(["-Degl=enabled", "-Dgbm=enabled", "-Ddri3=enabled"])
            args_platforms.append("surfaceless")
        else:
            args.extend(["-Degl=disabled", "-Dgbm=disabled", "-Ddri3=disabled"])

        args.append(opt_bool("+opengl" in spec, "opengl"))
        args.append(opt_enable("+opengles" in spec, "gles1"))
        args.append(opt_enable("+opengles" in spec, "gles2"))

        args.append(opt_enable(num_frontends > 1, "shared-glapi"))

        if "+llvm" in spec:
            llvm_config = Executable(spec["libllvm"].prefix.bin.join("llvm-config"))
            # Fix builds on hosts where /usr/bin/llvm-config-* is found and provides an
            # incompatible version. Ensure that the llvm-config of spec['libllvm'] is
            # used.
            args.append("--native-file")
            args.append("meson-native-config.ini")
            mkdirp(self.build_directory)
            with working_dir(self.build_directory):
                with open("meson-native-config.ini", "w") as native_config:
                    native_config.write("[binaries]\n")
                    native_config.write("llvm-config = '{0}'\n".format(llvm_config.path))
            args.append("-Dllvm=enabled")
            args.append(opt_enable("+llvm_dylib" in spec["libllvm"], "shared-llvm"))

            # Match the llvm rtti setting
            if llvm_config("--has-rtti", error=str, output=str).strip() == "YES":
                args.append("-Dcpp_rtti=true")
            else:
                args.append("-Dcpp_rtti=false")
        else:
            args.append("-Dllvm=disabled")

        args_swr_arches = []
        if "swr=auto" in spec:
            if "avx" in spec.target:
                args_swr_arches.append("avx")
            if "avx2" in spec.target:
                args_swr_arches.append("avx2")
            if "avx512f" in spec.target:
                if "avx512er" in spec.target:
                    args_swr_arches.append("knl")
                if "avx512bw" in spec.target:
                    args_swr_arches.append("skx")
        else:
            if "swr=avx" in spec:
                args_swr_arches.append("avx")
            if "swr=avx2" in spec:
                args_swr_arches.append("avx2")
            if "swr=knl" in spec:
                args_swr_arches.append("knl")
            if "swr=skx" in spec:
                args_swr_arches.append("skx")

        if args_swr_arches:
            args_gallium_drivers.append("swr")
            args.append("-Dswr-arches=" + ",".join(args_swr_arches))

        # Add the remaining list args
        args.append("-Dplatforms=" + ",".join(args_platforms))
        args.append("-Dgallium-drivers=" + ",".join(args_gallium_drivers))
        if args_dri_drivers:
            args.append("-Ddri-drivers=" + ",".join(args_dri_drivers))

        return args
