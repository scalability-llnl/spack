# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tesseract(AutotoolsPackage):
    """Tesseract Open Source OCR Engine."""

    homepage = "https://github.com/tesseract-ocr/tesseract"
    url = "https://github.com/tesseract-ocr/tesseract/archive/4.1.1.tar.gz"

    license("Apache-2.0")

    version("4.1.1", sha256="2a66ff0d8595bff8f04032165e6c936389b1e5727c3ce5a27b3e059d218db1cb")
    version("4.1.0", sha256="5c5ed5f1a76888dc57a83704f24ae02f8319849f5c4cf19d254296978a1a1961")
    version("4.0.0", sha256="a1f5422ca49a32e5f35c54dee5112b11b99928fc9f4ee6695cdc6768d69f61dd")

    depends_on("cxx", type="build")  # generated

    # do not fetch the jar files from Makefile
    patch("java_Makefile.patch")

    jars = ["piccolo2d-core-3.0.1", "piccolo2d-extras-3.0.1", "jaxb-api-2.3.1"]
    resource(
        name=jars[0],
        url="https://search.maven.org/remotecontent?filepath=org/piccolo2d/piccolo2d-core/3.0.1/piccolo2d-core-3.0.1.jar",
        sha256="9acad723136ddb996e96f5d488b9b046753a1d4c60ea639d5e3f9701deaf60ad",
        placement=jars[0],
        expand=False,
    )
    resource(
        name=jars[1],
        url="https://search.maven.org/remotecontent?filepath=org/piccolo2d/piccolo2d-extras/3.0.1/piccolo2d-extras-3.0.1.jar",
        sha256="ba45f343e9ebc06c9b4ce165c8bb539b11cbf59e93d1df48489ab173f74375a8",
        placement=jars[1],
        expand=False,
    )
    resource(
        name=jars[2],
        url="https://search.maven.org/remotecontent?filepath=javax/xml/bind/jaxb-api/2.3.1/jaxb-api-2.3.1.jar",
        sha256="88b955a0df57880a26a74708bc34f74dcaf8ebf4e78843a28b50eae945732b06",
        placement=jars[2],
        expand=False,
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("doxygen", type="build")
    depends_on("asciidoc", type="build")
    depends_on("libxslt", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("leptonica")
    depends_on("libarchive")
    depends_on("curl")
    depends_on("icu4c")
    depends_on("cairo")
    depends_on("pango")
    depends_on("java")

    def autoreconf(self, spec, prefix):
        autogen = Executable(join_path(".", "autogen.sh"))
        autogen()

    def setup_run_environment(self, env):
        env.set("SCROLLVIEW_PATH", prefix.share.tessdata)

    @run_after("install")
    def training(self):
        make("training")
        make("training-install")

        # move the jar files to the java directory
        for jar in self.jars:
            src = "{0}/{1}/{2}.jar".format(self.stage.source_path, jar, jar)
            dest = "{0}/java/{1}.jar".format(self.stage.source_path, jar)
            copy(src, dest)

        with working_dir("java"):
            make("install-jars")
