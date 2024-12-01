# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ant(Package):
    """Apache Ant is a Java library and command-line tool whose mission is to
    drive processes described in build files as targets and extension points
    dependent upon each other
    """

    homepage = "https://ant.apache.org/"
    url = "https://archive.apache.org/dist/ant/source/apache-ant-1.9.7-src.tar.gz"

    license("Apache-2.0")

    version("1.10.14", sha256="9a5fe31f44d1eb62590cbe38e4fab25b25e2f68643b38a54b66498e0bf621b54")
    version("1.10.13", sha256="da006f4c888d41d0f3f213565e48aeff73e4d8a6196e494121d8da1e567a8406")

    # https://nvd.nist.gov/vuln/detail/CVE-2020-1945
    version(
        "1.10.7",
        sha256="2f9c4ef094581663b41a7412324f65b854f17622e5b2da9fcb9541ca8737bd52",
        deprecated=True,
    )
    version(
        "1.10.6",
        sha256="c641721ae844196b28780e7999d2ae886085b89433438ab797d531413a924311",
        deprecated=True,
    )
    version(
        "1.10.5",
        sha256="5937cf11d74d75d6e8927402950b012e037e362f9f728262ce432ad289b9f6ca",
        deprecated=True,
    )
    version(
        "1.10.4",
        sha256="b0718c6c1b2b8d3bc77cd1e30ea183cd7741cfb52222a97c754e02b8e38d1948",
        deprecated=True,
    )
    version(
        "1.10.3",
        sha256="988b0cac947559f7347f314b9a3dae1af0dfdcc254de56d1469de005bf281c5a",
        deprecated=True,
    )
    version(
        "1.10.2",
        sha256="f3cf217b9befae2fef7198b51911e33a8809d98887cc971c8957596f459c6285",
        deprecated=True,
    )
    version(
        "1.10.1",
        sha256="68f7ced0aa15d1f9f672f23d67c86deaf728e9576936313cfbff4f7a0e6ce382",
        deprecated=True,
    )
    version(
        "1.10.0",
        sha256="1f78036c38753880e16fb755516c8070187a78fe4b2e99b59eda5b81b58eccaf",
        deprecated=True,
    )
    version(
        "1.9.9",
        sha256="d6a0c93777ab27db36212d77c5733ac80d17fe24e83f947df23a8e0ad4ac48cc",
        deprecated=True,
    )
    version(
        "1.9.8",
        sha256="5f4daf56e66fc7a71de772920ca27c15eac80cf1fcf41f3b4f2d535724942681",
        deprecated=True,
    )
    version(
        "1.9.7",
        sha256="648b3f3787bb0cb6226978b6d4898eb7e21ae391385357a5f824972dd910a1c8",
        deprecated=True,
    )
    version(
        "1.9.6",
        sha256="550d2aaf828785e30870c227056942c2a552da961db6010cedb2fbcfa8e3268d",
        deprecated=True,
    )

    depends_on("java")

    def install(self, spec, prefix):
        env["ANT_HOME"] = self.prefix
        bash = which("bash")
        bash("./build.sh", "install-lite")
