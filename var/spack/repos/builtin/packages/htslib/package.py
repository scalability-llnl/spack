# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Htslib(AutotoolsPackage):
    """C library for high-throughput sequencing data formats."""

    maintainers("jbeal-work")

    homepage = "https://github.com/samtools/htslib"
    url = "https://github.com/samtools/htslib/releases/download/1.13/htslib-1.13.tar.bz2"

    license("MIT AND BSD-3-Clause-Modification")

    version("1.20", sha256="e52d95b14da68e0cfd7d27faf56fef2f88c2eaf32a2be51c72e146e3aa928544")
    version("1.19.1", sha256="222d74d3574fb67b158c6988c980eeaaba8a0656f5e4ffb76b5fa57f035933ec")
    version("1.19", sha256="8751c40c4fa7d1f23a6864c5b20a73744f8be68239535ae7729c5f7d394d0736")
    version("1.18", sha256="f1ab53a593a2320a1bfadf4ef915dae784006c5b5c922c8a8174d7530a9af18f")
    version("1.17", sha256="763779288c40f07646ec7ad98b96c378c739171d162ad98398868783b721839f")
    version("1.16", sha256="606b7c7aff73734cf033ecd156f40529fa5792f54524952a28938ca0890d7924")
    version("1.15.1", sha256="8d7f8bf9658226942eeab70af2a22aca618577eaa8fe2ed9416ee306d5351aa1")
    version("1.15", sha256="1a9f49911503a22f56817cc82ea9b87fb7e7467b5ff989ca5aa61c12e7d532d9")
    version("1.14", sha256="ed221b8f52f4812f810eebe0cc56cd8355a5c9d21c62d142ac05ad0da147935f")
    version("1.13", sha256="f2407df9f97f0bb6b07656579e41a1ca5100464067b6b21bf962a2ea4b0efd65")
    version("1.12", sha256="2280141b46e953ba4ae01b98335a84f8e6ccbdb6d5cdbab7f70ee4f7e3b6f4ca")
    version("1.11", sha256="cffadd9baa6fce27b8fe0b01a462b489f06a5433dfe92121f667f40f632538d7")
    version("1.10.2", sha256="e3b543de2f71723830a1e0472cf5489ec27d0fbeb46b1103e14a11b7177d1939")
    version("1.9", sha256="e04b877057e8b3b8425d957f057b42f0e8509173621d3eccaedd0da607d9929a")
    version("1.8", sha256="c0ef1eec954a98cc708e9f99f6037db85db45670b52b6ab37abcc89b6c057ca1")
    version("1.7", sha256="be3d4e25c256acdd41bebb8a7ad55e89bb18e2fc7fc336124b1e2c82ae8886c6")
    version("1.6", sha256="9588be8be0c2390a87b7952d644e7a88bead2991b3468371347965f2e0504ccb")
    version("1.5", sha256="a02b515ea51d86352b089c63d778fb5e8b9d784937cf157e587189cb97ad922d")
    version("1.4", sha256="5cfc8818ff45cd6e924c32fec2489cb28853af8867a7ee8e755c4187f5883350")
    version("1.3.1", sha256="49d53a2395b8cef7d1d11270a09de888df8ba06f70fe68282e8235ee04124ae6")
    version("1.2", sha256="125c01421d5131afb4c3fd2bc9c7da6f4f1cd9ab5fc285c076080b9aca24bffc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "libcurl",
        default=True,
        description="Enable libcurl-based support for http/https/etc URLs,"
        " for versions >= 1.3. This also enables S3 and GCS support by default.",
    )
    variant(
        "libdeflate",
        default=True,
        description="use libdeflate for faster crc and deflate algorithms",
    )
    variant("gcs", default=True, description="enable gcs url support", when="@1.5:+libcurl")
    variant("s3", default=True, description="enable s3 url support", when="@1.5:+libcurl")
    variant("plugins", default=False, description="enable support for separately compiled plugins")
    variant("pic", default=True, description="Compile with PIC support")

    depends_on("zlib-api")
    depends_on("bzip2", when="@1.4:")
    depends_on("xz", when="@1.4:")
    depends_on("curl", when="@1.3:+libcurl")
    depends_on("openssl", when="+s3")
    depends_on("libdeflate", when="@1.8:+libdeflate")

    depends_on("m4", when="@1.2")
    depends_on("autoconf", when="@1.2")
    depends_on("automake", when="@1.2")
    depends_on("libtool", when="@1.2")

    conflicts("zlib-ng", when="@:1.12")  # https://github.com/samtools/htslib/issues/1257

    @property
    def libs(self):
        return find_libraries("libhts", root=self.prefix, recursive=True)

    # v1.2 uses the automagically assembled tarball from .../archive/...
    # everything else uses the tarballs uploaded to the release
    def url_for_version(self, version):
        if version.string == "1.2":
            return "https://github.com/samtools/htslib/archive/1.2.tar.gz"
        else:
            url = "https://github.com/samtools/htslib/releases/download/{0}/htslib-{0}.tar.bz2"
            return url.format(version.dotted)

    def flag_handler(self, name, flags):
        if name == "cflags" and self.spec.satisfies("+pic"):
            flags.append(self.compiler.cc_pic_flag)
        return (flags, None, None)

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("@1.3:"):
            args.extend(self.enable_or_disable("libcurl"))

        if spec.satisfies("@1.5:"):
            args.extend(self.enable_or_disable("s3"))
            args.extend(self.enable_or_disable("gcs"))
            args.extend(self.enable_or_disable("plugins"))

        if spec.satisfies("@1.8:"):
            args.extend(self.enable_or_disable("libdeflate"))

        return args
