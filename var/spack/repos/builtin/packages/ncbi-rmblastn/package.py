# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NcbiRmblastn(AutotoolsPackage):
    """RMBlast search engine for NCBI"""

    homepage = "https://www.repeatmasker.org/rmblast/"
    url = (
        "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/ncbi-blast-2.9.0+-src.tar.gz"
    )

    version("2.14.0", sha256="bf477f1b0c3b82f0b7a7094bf003a9a83e37e3b0716c1df799060c4feab17500")
    version("2.11.0", sha256="d88e1858ae7ce553545a795a2120e657a799a6d334f2a07ef0330cc3e74e1954")
    version("2.9.0", sha256="a390cc2d7a09422759fc178db84de9def822cbe485916bbb2ec0d215dacdc257")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    maintainers("snehring")

    # There is a corresponding gzipped patch file associated with each version.
    # According to the documentation, https://www.repeatmasker.org/RMBlast.html,
    # Download NCBI Blast+ and rmblast patch file:
    #   ncbi-blast-2.11.0+-src.tar.gz
    #   isb-2.11.0+-rmblast.patch.gz
    # The patch is downloaded and unzipped in the ncbi-rmblastn Spack package
    # directory to make it available for the patch directive.
    patch(
        "https://www.repeatmasker.org/rmblast/isb-2.14.0+-rmblast.patch.gz",
        sha256="cd083f256551c6d6021897a1b08e023976e82c59576787d4885f57d36f9e6fdf",
        archive_sha256="9de0e67467a4cffdde0c5f67e3658fb52ed313e4550f9a36a251bddb2ba33f49",
        when="@2.14.0",
    )
    patch(
        "https://www.repeatmasker.org/isb-2.11.0+-rmblast.patch.gz",
        sha256="ce985abd3512834adb9ad3e4078fbf9608a33a2ee6538a1e94b641490c92f899",
        archive_sha256="0fc27781c2ea2f17645247e2f3775b5d18c56f0b62761a865347be745ea4f6be",
        when="@2.11.0",
    )
    patch(
        "https://www.repeatmasker.org/isb-2.9.0+-rmblast.patch.gz",
        sha256="ffa0845801aed11f4215b452532f3ff5b3dcb49ac8c14169568aaa585b9450ed",
        archive_sha256="e746ee480ade608052306fd21f015c8a323f27029f65399275216f9a4c882d59",
        when="@2.9.0",
    )

    patch("gcc13.patch", level=0, when="@2.14.0:%gcc@13:")

    depends_on("cpio", type="build")
    depends_on("boost")
    depends_on("lzo")
    depends_on("bzip2")
    depends_on("zstd")
    depends_on("xz")

    configure_directory = "c++"

    def url_for_version(self, version):
        url = (
            "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/{0}/ncbi-blast-{1}+-src.tar.gz"
        )
        return url.format(version, version)

    def configure_args(self):
        args = [
            "--with-mt",
            "--without-debug",
            "--without-krb5",
            "--without-openssl",
            "--without-libuv",
            "--with-projects=scripts/projects/rmblastn/project.lst",
        ]
        return args
