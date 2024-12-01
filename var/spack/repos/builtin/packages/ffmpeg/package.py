# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ffmpeg(AutotoolsPackage):
    """FFmpeg is a complete, cross-platform solution to record,
    convert and stream audio and video."""

    homepage = "https://ffmpeg.org"
    url = "https://ffmpeg.org/releases/ffmpeg-4.1.1.tar.bz2"
    git = "https://git.ffmpeg.org/ffmpeg.git"

    maintainers("xjrc")

    license("LGPL-2.1-or-later", when="~gpl", checked_by="wdconinc")
    license("LGPL-2.1-or-later AND GPL-2.0-or-later", when="+gpl", checked_by="wdconinc")

    version("master", branch="master")
    version("7.0.2", sha256="1ed250407ea8f955cca2f1139da3229fbc13032a0802e4b744be195865ff1541")
    version("7.0", sha256="a24d9074bf5523a65aaa9e7bd02afe4109ce79d69bd77d104fed3dab4b934d7a")
    version("6.1.1", sha256="5e3133939a61ef64ac9b47ffd29a5ea6e337a4023ef0ad972094b4da844e3a20")
    version("6.0", sha256="47d062731c9f66a78380e35a19aac77cebceccd1c7cc309b9c82343ffc430c3d")
    version("5.1.4", sha256="c3c1e316bf91468738dd0aff6eb1faab409f1edcd34fd1a4213626439bc5d743")
    version("5.1.3", sha256="5d5bef6a11f0c500588f9870ec965a30acc0d54d8b1e535da6554a32902d236d")
    version("5.1.2", sha256="39a0bcc8d98549f16c570624678246a6ac736c066cebdb409f9502e915b22f2b")
    version("4.4.4", sha256="47b1fbf70a2c090d9c0fae5910da11c6406ca92408bb69d8c935cd46c622c7ce")
    version("4.4.1", sha256="8fc9f20ac5ed95115a9e285647add0eedd5cc1a98a039ada14c132452f98ac42")
    version("4.3.2", sha256="ab3a6d6a70358ba0a5f67f37f91f6656b7302b02e98e5b8c846c16763c99913a")
    version("4.2.2", sha256="b620d187c26f76ca19e74210a0336c3b8380b97730df5cdf45f3e69e89000e5c")
    version("4.1.1", sha256="0cb40e3b8acaccd0ecb38aa863f66f0c6e02406246556c2992f67bf650fab058")
    version("4.1", sha256="b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5")
    version("3.4.13", sha256="f640aa6f92323558ee31314b773cf2e935def620474754b929e815f8f1ec933f")
    version("3.4.12", sha256="08e400330c70b567116addebd1a70279e0d41b0f8742085e32527f2a4eef9ca3")
    version("3.2.19", sha256="87a61fa3b20819b71633aa90b55ee6411614e4a0ff7908cf35236b465de5e602")
    version("3.2.4", sha256="c0fa3593a2e9e96ace3c1757900094437ad96d1d6ca19f057c378b5f394496a4")
    version("2.8.22", sha256="c56534d2862d2690b28875e142e0364ab86d784a22775449f04bf995efbc7064")
    version("2.8.21", sha256="782c3af1a1ee8945be0800edc39b1d1199ee6a8f31c74b65230795f11911b0d8")
    version("2.8.15", sha256="35647f6c1f6d4a1719bc20b76bf4c26e4ccd665f46b5676c0e91c5a04622ee21")
    version("1.0.10", sha256="1dbde434c3b5c573d3b2ffc1babe3814f781c10c4bc66193a4132a44c9715176")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Licensing
    variant(
        "gpl",
        default=True,
        description="allow use of GPL code, the resulting libs and binaries will be under GPL",
    )
    variant("version3", default=True, description="upgrade (L)GPL to version 3")
    variant(
        "nonfree",
        default=False,
        description="allow use of nonfree code, the resulting libs "
        "and binaries will be unredistributable",
    )

    # NOTE: The libopencv option creates a circular dependency.
    # NOTE: There are more possible variants that would require additional
    # spack packages.

    # meta variants: These will toggle several settings
    variant("X", default=False, when="@2.4:", description="X11 support")
    variant("drawtext", default=False, description="drawtext filter")

    # options
    variant("bzlib", default=True, description="bzip2 support")
    variant("doc", default=False, description="build documentation")
    variant("libaom", default=False, when="@4.0:", description="AV1 video encoding/decoding")
    variant("libmp3lame", default=False, description="MP3 encoding")
    variant("libopenjpeg", default=False, description="JPEG 2000 de/encoding")
    variant("libopus", default=False, description="Opus de/encoding")
    variant(
        "libsnappy",
        default=False,
        when="@2.7:",
        description="Snappy compression, needed for hap encoding",
    )
    variant("libspeex", default=False, description="Speex de/encoding")
    variant("libssh", default=False, when="@2.1:", description="SFTP protocol")
    variant("libvorbis", default=False, description="Vorbis en/decoding")
    variant("libvpx", default=False, description="VP9 en/decoding")
    variant("libwebp", default=False, when="@2.2:", description="WebP encoding via libwebp")
    variant("libxml2", default=False, description="XML parsing, needed for dash demuxing support")
    variant("libzmq", default=False, when="@2.0:", description="message passing via libzmq")
    variant("lzma", default=False, when="@2.4:", description="lzma support")
    variant("avresample", default=False, when="@0.11:4.4", description="AV reasmpling component")
    variant("openssl", default=False, description="needed for https support")
    variant("sdl2", default=False, when="@3.2:", description="sdl2 support")
    variant("shared", default=True, description="build shared libraries")
    variant("libx264", default=False, description="H.264 encoding")

    conflicts("@1", when="platform=darwin target=aarch64:", msg="requires gas-preprocessor")

    depends_on("alsa-lib", when="platform=linux")
    depends_on("iconv")
    depends_on("yasm@1.2.0:")
    depends_on("zlib-api")

    depends_on("pkgconfig", type="build")

    depends_on("aom", when="+libaom")
    depends_on("bzip2", when="+bzlib")
    depends_on("fontconfig", when="+drawtext")
    depends_on("freetype", when="+drawtext")
    depends_on("fribidi", when="+drawtext")
    depends_on("lame", when="+libmp3lame")
    depends_on("libssh", when="+libssh")
    depends_on("libvorbis", when="+libvorbis")
    depends_on("libvpx", when="+libvpx")
    depends_on("libwebp", when="+libwebp")
    depends_on("libxml2", when="+libxml2")
    depends_on("libxv", when="+X")
    depends_on("libzmq", when="+libzmq")
    depends_on("openjpeg", when="+libopenjpeg")
    depends_on("openssl", when="+openssl")
    depends_on("opus", when="+libopus")
    depends_on("sdl2@:2.0.22", when="@3.2:4.4+sdl2")
    depends_on("sdl2", when="+sdl2")
    depends_on("snappy", when="+libsnappy")
    depends_on("speex", when="+libspeex")
    depends_on("xz", when="+lzma")
    depends_on("x264", when="+libx264")
    depends_on("texinfo", when="+doc")
    depends_on("texinfo@:6", when="+doc @:4")

    conflicts("%nvhpc")

    # Solve build failure against vulkan headers 1.3.279
    patch(
        "https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff_plain/fef22c87ada4",
        sha256="5726e8e999e3fc7a5ae4c4c846c9151246e5846c54dc3b8ff8326ee31c59631a",
        when="@6.1.1",
    )

    # Patch solving a build failure when vulkan is enabled
    patch(
        "https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff_plain/eb0455d64690",
        sha256="967d25a67297c53dde7151f7bc5eb37ae674525ee468880f973b9ebc3e12ed2c",
        when="@5.1.2",
    )

    # Patch fixing a build failure with binutils 2.41.0
    patch(
        "https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff_plain/effadce6c756247ea8bae32dc13bb3e6f464f0eb",
        sha256="f070ac16be68b4d32b1b5b885d146eb36eb508daa928b6f0f78256c3482f9f0e",
        when="@6:6.0",
    )
    # Patch fixing a build failure with binutils 2.41.0, already in @5.1.4
    patch(
        "https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff_plain/effadce6c756247ea8bae32dc13bb3e6f464f0eb",
        sha256="f070ac16be68b4d32b1b5b885d146eb36eb508daa928b6f0f78256c3482f9f0e",
        when="@:5.1.3",
    )

    # fix incompatibility with texinfo@7, especially @7.1:
    patch(
        "https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff_plain/f01fdedb69e4accb1d1555106d8f682ff1f1ddc7",
        sha256="673813d13f5c37b75ff5bcb56790ccd6b16962fdb9bddcbbeeead979d47d31b3",
        when="@6.0",
    )
    patch(
        "https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff_plain/f01fdedb69e4accb1d1555106d8f682ff1f1ddc7",
        sha256="673813d13f5c37b75ff5bcb56790ccd6b16962fdb9bddcbbeeead979d47d31b3",
        when="@5:5.1.3",
    )

    @property
    def libs(self):
        return find_libraries("*", self.prefix, recursive=True)

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include]
        return headers

    @when("@:6.0 %apple-clang@15:")
    def setup_build_environment(self, env):
        if self.spec.satisfies("@:3"):
            env.append_flags("CFLAGS", "-Wno-error=incompatible-function-pointer-types")

    def enable_or_disable_meta(self, variant, options):
        switch = "enable" if "+{0}".format(variant) in self.spec else "disable"
        return ["--{0}-{1}".format(switch, option) for option in options]

    def configure_args(self):
        spec = self.spec
        config_args = ["--enable-pic", "--cc={0}".format(spack_cc), "--cxx={0}".format(spack_cxx)]

        # '+X' meta variant #

        xlib_opts = []

        if spec.satisfies("@2.5:"):
            xlib_opts.extend(["libxcb", "libxcb-shape", "libxcb-shm", "libxcb-xfixes", "xlib"])

        config_args += self.enable_or_disable_meta("X", xlib_opts)

        # '+drawtext' meta variant #

        drawtext_opts = [
            "{0}fontconfig".format("lib" if spec.satisfies("@3:") else ""),
            "libfreetype",
        ]

        if spec.satisfies("@2.3:"):
            drawtext_opts.append("libfribidi")

        config_args += self.enable_or_disable_meta("drawtext", drawtext_opts)

        # other variants #

        variant_opts = [
            "bzlib",
            "doc",
            "gpl",
            "libmp3lame",
            "libopenjpeg",
            "libopus",
            "libspeex",
            "libvorbis",
            "libvpx",
            "libx264",
            "nonfree",
            "openssl",
            "shared",
            "version3",
            "avresample",
            "libzmq",
            "libssh",
            "libwebp",
            "lzma",
            "libsnappy",
            "sdl2",
            "libaom",
        ]

        if spec.satisfies("@4:"):
            variant_opts.append("libxml2")

        for variant_opt in variant_opts:
            config_args += self.enable_or_disable(variant_opt)

        return config_args
