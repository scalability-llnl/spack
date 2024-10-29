# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libva(AutotoolsPackage):
    """Libva is an implementation for VA-API (Video Acceleration API).
    VA-API is an open-source library and API specification, which provides
    access to graphics hardware acceleration capabilities for video
    processing. It consists of a main library and driver-specific
    acceleration backends for each supported hardware vendor."""

    homepage = "https://github.com/intel/libva"
    url = "https://github.com/intel/libva/archive/refs/tags/2.22.0.tar.gz"

    version("2.22.0", sha256="467c418c2640a178c6baad5be2e00d569842123763b80507721ab87eb7af8735")
    version("2.21.0", sha256="f7c3fffef3f04eb146e036dad2587d852bfb70e4926d014bf437244915ef7425")
    version("2.20.0", sha256="117f8d658a5fc9ea406ca80a3eb4ae1d70b15a54807c9ed77199c812bed73b60")
    version("2.19.0", sha256="8cb5e2a9287a76b12c0b6cb96f4f27a0321bbe693df43cd950e5d4542db7f227")
    version("2.18.0", sha256="9d666c70c12dfefcdd27ae7dea771557f75e24961d0ed4cb050d96fb6136f438")
    version("2.17.0", sha256="8940541980ef998a36cd8f6ad905e81838ea4ddf56dc479ed2bebd12711e6001")
    version("2.16.0", sha256="766edf51fd86efe9e836a4467d4ec7c3af690a3c601b3c717237cee856302279")
    version("2.15.0", sha256="869aaa9b9eccb1cde63e1c5b0ac0881cefc00156010bb49f6dce152471770ba8")
    version("2.14.0", sha256="f21152a2170edda9d1c4dd463d52eaf62b553e83e553c0a946654523cca86d5e")
    version("2.13.0", sha256="6b7ec7d4fa204dad3f266450981f1f0892400c03afd3e00ac11f8ccade5aaaa1")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libdrm")
    depends_on("libx11", when="^[virtuals=gl] glx")
    depends_on("libxext", when="^[virtuals=gl] glx")

    def autoreconf(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()

    def configure_args(self):
        spec = self.spec
        args = [
            "--disable-x11",
            "--disable-wayland",
            "--disable-glx",
            "--enable-libdrm",
        ]
        if spec.satisfies("^[virtuals=gl] glx"):
            args.append("--enable-x11")
        else:
            args.append("--disable-x11")
        return args
