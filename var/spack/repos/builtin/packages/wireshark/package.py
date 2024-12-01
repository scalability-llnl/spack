# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Wireshark(CMakePackage):
    """Graphical network analyzer and capture tool"""

    homepage = "https://www.wireshark.org"
    url = "https://www.wireshark.org/download/src/all-versions/wireshark-2.6.0.tar.xz"

    license("GPL-2.0-or-later")

    version("3.2.1", sha256="589f640058d6408ebbd695a80ebbd6e7bd99d8db64ecda253d27100dfd27e85b")
    version("3.2.0", sha256="4cfd33a19a454ff4002243e9d04d6afd64280a109a21ae652a192f2be2b1b66c")
    version("3.1.0", sha256="a7b54f9e35fc69291dcac5104ecbef8260534a75dec5b8105605b6c423fd3de3")
    version("3.0.8", sha256="b4bd8189934d82330a053c5b10398f2b625b1e1c8818831ab61739b2d7aa7561")
    version("2.6.0", sha256="711c7f01d27a8817d58277a5487cef3e3c7bab1c8caaf8f4c92aa21015b9117f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("libssh", default=False, description="Build with libssh")
    variant("nghttp2", default=False, description="Build with nghttp2")
    variant("qt", default=False, description="Build with qt")
    variant("headers", default=True, description="Install headers")

    depends_on("bison", type="build")
    depends_on("c-ares")
    depends_on("doxygen", type="build")
    depends_on("flex", type="build")
    depends_on("git", type="build")
    depends_on("glib")
    depends_on("gnutls")
    depends_on("libgcrypt@1.4.2:")
    depends_on("libmaxminddb")
    depends_on("libtool@2.2.2:", type="build")
    depends_on("libpcap")
    depends_on("lua@5.0.0:5.2")
    depends_on("krb5")
    depends_on("pkgconfig", type="build")
    depends_on("libssh", when="+libssh")
    depends_on("nghttp2", when="+nghttp2")
    depends_on("qt@4.8:", when="+qt")

    def patch(self):
        # These try to capture from the network and run not compiled programs
        filter_file("suite_capture", "", "CMakeLists.txt")
        filter_file("suite_unittests", "", "CMakeLists.txt")

    def cmake_args(self):
        args = [
            "-DENEABLE_CARES=ON",
            "-DENABLE_GNUTLS=ON",
            "-DENABLE_LUA=ON",
            "-DENABLE_MAXMINDDB=ON",
            "-DYACC_EXECUTABLE=" + self.spec["bison"].prefix.bin.yacc,
            "-DGIT_EXECUTABLE=" + self.spec["git"].prefix.bin.git,
            "-DPCAP_INCLUDE_DIR=" + self.spec["libpcap"].prefix.include,
            "-DPCAP_LIB=" + str(self.spec["libpcap"].libs),
            "-DLUA_INCLUDE_DIR=" + self.spec["lua"].prefix.include,
            "-DLUA_LIBRARY=" + str(self.spec["lua"].libs),
            "-DBUILD_wireshark_gtk=OFF",
            "-DENABLE_PORTAUDIO=OFF",
            "-DENABLE_GTK3=OFF",
            "-DBUILD_SMI=OFF",
        ]

        if self.spec.satisfies("+qt"):
            args.append("-DBUILD_wireshark=ON")
            args.append("-DENABLE_APPLICATION_BUNDLE=ON")
            if self.spec["qt"].version >= Version("5"):
                args.append("-DENABLE_QT5=ON")
            else:
                args.append("-DENABLE_QT5=OFF")
        else:
            args.append("-DBUILD_wireshark=OFF")
            args.append("-DENABLE_APPLICATION_BUNDLE=OFF")
            args.append("-DENABLE_QT5=OFF")

        if self.spec.satisfies("+libssh"):
            args.append("-DBUILD_sshdump=ON")
            args.append("-DBUILD_ciscodump=ON")
        else:
            args.append("-DBUILD_sshdump=OFF")
            args.append("-DBUILD_ciscodump=OFF")

        if self.spec.satisfies("+nghttp2"):
            args.append("-DBUILD_NGHTTP2=ON")
        else:
            args.append("-DBUILD_NGHTTP2=OFF")

        return args

    @run_after("install")
    def symlink(self):
        if self.spec.satisfies("platform=darwin"):
            link(
                join_path(self.prefix, "Wireshark.app/Contents/MacOS/Wireshark"),
                self.prefix.bin.wireshark,
            )

    @run_after("install")
    def install_headers(self):
        if self.spec.satisfies("+headers"):
            folders = [
                ".",
                "epan/crypt",
                "epan/dfilter",
                "epan/dissectors",
                "epan/ftypes",
                "epan/wmem",
                "wiretap",
                "wsutil",
            ]
            for folder in folders:
                mkdirp(join_path(prefix.include.wireshark, folder))
                install(join_path(folder, "*.h"), join_path(prefix.include.wireshark, folder))
