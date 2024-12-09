# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxslt(AutotoolsPackage):
    """Libxslt is the XSLT C library developed for the GNOME project. XSLT
    itself is a an XML language to define transformation for XML. Libxslt is
    based on libxml2 the XML C library developed for the GNOME project. It also
    implements most of the EXSLT set of processor-portable extensions functions
    and some of Saxon's evaluate and expressions extensions."""

    homepage = "https://gitlab.gnome.org/GNOME/libxslt/-/wikis/home"
    url = "https://download.gnome.org/sources/libxslt/1.1/libxslt-1.1.34.tar.xz"
    git = "https://gitlab.gnome.org/GNOME/libxslt"
    list_url = "https://download.gnome.org/sources/libxslt/"
    list_depth = 1

    license("X11", checked_by="wdconinc")

    version("1.1.42", sha256="85ca62cac0d41fc77d3f6033da9df6fd73d20ea2fc18b0a3609ffb4110e1baeb")
    version("1.1.41", sha256="3ad392af91115b7740f7b50d228cc1c5fc13afc1da7f16cb0213917a37f71bda")
    version("1.1.40", sha256="194715db023035f65fb566402f2ad2b5eab4c29d541f511305c40b29b1f48d13")
    version("1.1.39", sha256="2a20ad621148339b0759c4d4e96719362dee64c9a096dbba625ba053846349f0")
    version("1.1.38", sha256="1f32450425819a09acaff2ab7a5a7f8a2ec7956e505d7beeb45e843d0e1ecab1")
    version("1.1.37", sha256="3a4b27dc8027ccd6146725950336f1ec520928f320f144eb5fa7990ae6123ab4")
    version("1.1.36", sha256="12848f0a4408f65b530d3962cd9ff670b6ae796191cfeff37522b5772de8dc8e")
    version("1.1.35", sha256="8247f33e9a872c6ac859aa45018bc4c4d00b97e2feac9eebc10c93ce1f34dd79")
    version("1.1.34", sha256="98b1bd46d6792925ad2dfe9a87452ea2adebf69dcb9919ffd55bf926a7f93f7f")
    version("1.1.33", sha256="8e36605144409df979cab43d835002f63988f3dc94d5d3537c12796db90e38c8")
    version("1.1.32", sha256="526ecd0abaf4a7789041622c3950c0e7f2c4c8835471515fd77eec684a355460")
    version("1.1.29", sha256="b5976e3857837e7617b29f2249ebb5eeac34e249208d31f1fbf7a6ba7a4090ce")
    version("1.1.28", sha256="5fc7151a57b89c03d7b825df5a0fae0a8d5f05674c0e7cf2937ecec4d54a028c")
    version("1.1.26", sha256="55dd52b42861f8a02989d701ef716d6280bfa02971e967c285016f99c66e3db1")

    depends_on("c", type="build")

    variant("crypto", default=True, description="Build libexslt with crypto support")
    variant("python", default=False, description="Build Python bindings")

    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("iconv")
    depends_on("libxml2")
    depends_on("libxml2+python", when="+python")
    depends_on("xz")
    depends_on("zlib-api")
    depends_on("libgcrypt", when="+crypto")

    depends_on("python+shared", when="+python")
    extends("python", when="+python")

    def url_for_version(self, v):
        if v > Version("1.1.34"):
            return f"https://download.gnome.org/sources/libxslt/{v.up_to(2)}/libxslt-{v}.tar.xz"
        else:
            return f"http://xmlsoft.org/sources/libxslt-{v}.tar.gz"

    def configure_args(self):
        args = []

        if self.spec.satisfies("+crypto"):
            args.append("--with-crypto")
        else:
            args.append("--without-crypto")

        if self.spec.satisfies("+python"):
            args.append("--with-python={0}".format(self.spec["python"].home))
        else:
            args.append("--without-python")

        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        if self.spec.satisfies("+python"):
            with working_dir("spack-test", create=True):
                python("-c", "import libxslt")

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file("-Wmissing-format-attribute", "", "configure")
