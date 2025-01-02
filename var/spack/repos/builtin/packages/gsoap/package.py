# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gsoap(AutotoolsPackage, SourceforgePackage):
    """The gSOAP toolkit is an extensive suite of portable C and C++
    software to develop XML Web services with powerful type-safe XML
    data bindings."""

    homepage = "https://www.genivia.com/products.html"

    sourceforge_mirror_path = "gsoap2/gsoap_2.8.127.zip"

    maintainers("greenc-FNAL", "gartung", "marcmengel", "vitodb")

    version("2.8.135", sha256="b11757e405d55d4674dfbf88c4fa6d7e24155cf64ed8ed578ccad2f2b555e98d")
    with default_args(deprecated=True):
        # Unavailable for direct download anymore
        version(
            "2.8.127", sha256="25ecad1bbc363494eb7ea95a68508e4c93cc20596fad9ebc196c6572bbbd3c08"
        )
        version(
            "2.8.124", sha256="4b798780989338f665ef8e171bbcc422a271004d62d5852666d5eeca33a6a636"
        )
        version(
            "2.8.119", sha256="8997c43b599a2bfe4a788e303a5dd24bbf5992fd06d56f606ca680ca5b0070cf"
        )
        version(
            "2.8.114", sha256="aa70a999258100c170a3f8750c1f91318a477d440f6a28117f68bc1ded32327f"
        )
        version(
            "2.8.113", sha256="e73782b618303cf55ea6a45751b75ba96797a7a12967ed9d02e6d5761977e73a"
        )
        version(
            "2.8.112", sha256="05345312e0bb4d81c98ae63b97cff9eb097f38dafe09356189f9d8e235c54095"
        )
        version(
            "2.8.111", sha256="f1670c7e3aeaa66bc5658539fbd162e5099f022666855ef2b2c2bac07fec4bd3"
        )

    depends_on("openssl")
    depends_on("pkgconfig", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")

    def configure_args(self):
        return ["--enable-ipv6"]

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("PKG_CONFIG_PATH", "%s/lib/ldconfig" % self.prefix)

    def flag_handler(self, name, flags):
        if name in ["cflags", "cxxflags", "cppflags"]:
            flags.append(self.compiler.cc_pic_flag)

        return self.build_system_flags(name, flags)
