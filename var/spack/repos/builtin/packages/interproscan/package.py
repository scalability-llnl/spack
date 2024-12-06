# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Interproscan(Package):
    """InterProScan is the software package that allows sequences
    (protein and nucleic) to be scanned against InterPro's signatures.
    Signatures are predictive models, provided by several different
    databases, that make up the InterPro consortium. By default this
    does not download all the databases you likely want, you'll either
    want to build with +databases or download the data archive for the
    version you installed to a separate location and modify interproscan.properties"""

    homepage = "https://www.ebi.ac.uk/interpro/interproscan.html"
    url = "https://github.com/ebi-pf-team/interproscan/archive/5.36-75.0.tar.gz"
    maintainers("snehring")

    license("Apache-2.0")

    version("5.63-95.0", sha256="3d7babd09e64da3d7104c58f1e5104a298d69425e3210952331bc3f1ddf89ca6")
    version("5.61-93.0", sha256="70aca3b14983733fe5119b6978cb707156d006d7f737aa60ce6c9addd6c288e4")
    version("5.56-89.0", sha256="75e6a8f86ca17356a2f77f75b07d6d8fb7b397c9575f6e9716b64983e490b230")
    version("5.38-76.0", sha256="cb191ff8eee275689b789167a57b368ea5c06bbcd36b4de23e8bbbbdc0fc7434")
    version("5.36-75.0", sha256="383d7431e47c985056c856ceb6d4dcf7ed2559a4a3d5c210c01ce3975875addb")
    version(
        "4.8",
        sha256="f1cb0ae1218eb05ed59ad7f94883f474eb9a6185a56ad3a93a364acb73506a3f",
        url="ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/4/RELEASE/4.8/iprscan_v4.8.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    resource(
        when="@5.63-95.0 +databases",
        name="databases",
        url="https://ftp.ebi.ac.uk/pub/databases/interpro/iprscan/5/5.63-95.0/alt/interproscan-data-5.63-95.0.tar.gz",
        sha256="6048eabe2eeaa4630b7a6a0b34d8c5a1724b0d22bba318c04c43777368e16cc4",
    )

    resource(
        when="@5.61-93.0 +databases",
        name="databases",
        url="https://ftp.ebi.ac.uk/pub/databases/interpro/iprscan/5/5.61-93.0/alt/interproscan-data-5.61-93.0.tar.gz",
        sha256="064aa4b4c3b2e27b457298359087878e48fc785bff801c95691f090d1b83867d",
    )

    resource(
        when="@5.56-89.0 +databases",
        name="databases",
        url="https://ftp.ebi.ac.uk/pub/databases/interpro/iprscan/5/5.56-89.0/alt/interproscan-data-5.56-89.0.tar.gz",
        sha256="49cd0c69711f9469f3b68857f4581b23ff12765ca2b12893d18e5a9a5cd8032d",
    )

    resource(
        when="@5.38-76.0 +databases",
        name="databases",
        url="https://ftp.ebi.ac.uk/pub/databases/interpro/iprscan/5/5.38-76.0/alt/interproscan-data-5.38-76.0.tar.gz",
        sha256="e05e15d701037504f92ecf849c20317e70df28e78ff1945826b3c1e16d9b9cce",
    )

    resource(
        when="@5.36-75.0 +databases",
        name="databases",
        url="https://ftp.ebi.ac.uk/pub/databases/interpro/iprscan/5/5.36-75.0/alt/interproscan-data-5.36-75.0.tar.gz",
        sha256="e9b1e6f2d1c20d06661a31a08c973bc8ddf039a4cf1e45ec4443200375e5d6a4",
    )

    resource(
        when="@:4.8",
        name="binaries",
        url="https://ftp.ebi.ac.uk/pub/databases/interpro/iprscan/BIN/4.x/iprscan_bin4.x_Linux64.tar.gz",
        sha256="551610a4682b112522f3ded5268f76ba9a47399a72e726fafb17cc938a50e7ee",
    )

    variant(
        "databases",
        default=False,
        description="Fetch and include databases in the install. Greatly increases install size.",
    )

    depends_on("java@8.0:8.9", type=("build", "run"), when="@5:5.36-99.0")
    depends_on("java@11", type=("build", "run"), when="@5.37-76.0:")
    depends_on("maven", type="build", when="@5:")
    depends_on("perl@5:", type=("build", "run"))
    depends_on("python@3:", when="@5:", type=("build", "run"))
    depends_on("perl-cgi", when="@:4.8", type=("build", "run"))
    depends_on("perl-mailtools", when="@:4.8", type=("build", "run"))
    depends_on("perl-xml-quote", when="@:4.8", type=("build", "run"))
    depends_on("perl-xml-parser", when="@:4.8", type=("build", "run"))
    depends_on("perl-io-string", when="@:4.8", type=("build", "run"))
    depends_on("perl-io-stringy", when="@:4.8", type=("build", "run"))
    depends_on("perl-db-file", when="@:4.8", type=("build", "run"))

    patch("large-gid.patch", when="@5:")
    patch("non-interactive.patch", when="@:4.8")
    patch("ps_scan.patch", when="@:4.8")
    patch("web-pom.patch", when="@5:")

    def install(self, spec, prefix):
        with working_dir("core"):
            if self.run_tests:
                which("mvn")("verify")
            else:
                which("mvn")("clean", "install", "-DskipTests")
                with working_dir("jms-implementation"):
                    which("mvn")("clean", "package", "-DskipTests")

        target = join_path("core", "jms-implementation", "target", "interproscan-5-dist")
        install_tree(target, prefix)

        if spec.satisfies("+databases"):
            remove_directory_contents(prefix.data)
            install_tree(f"interproscan-{self.spec.version}/data", prefix.data)

        # link the main shell script into the PATH
        symlink(join_path(prefix, "interproscan.sh"), join_path(prefix.bin, "interproscan.sh"))

    @when("@:4.8")
    def install(self, spec, prefix):
        perl = which("perl")

        src = join_path(self.stage.source_path, "iprscan", "bin", "Linux")
        dst = join_path(self.stage.source_path, "bin", "binaries")
        force_symlink(src, dst)

        install_tree(".", prefix)

        with working_dir(prefix):
            perl("Config.pl")
