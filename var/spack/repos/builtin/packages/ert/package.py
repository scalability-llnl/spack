# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


version_to_hash_map = dict([("v1.1.0", "09663aad764d3c6cefa4d9de1f1213b5f03af9df")])


class Ert(Package):
    """The Empirical Roofline Tool, ERT, automatically generates roofline data for a given computer. This includes the
    maximum bandwidth for the various levels of the memory hierarchy and the maximum FLOP rate. This data is obtained
    using a variety of "micro-kernels".
    """

    homepage = "https://crd.lbl.gov/divisions/amcr/computer-science-amcr/par/research/roofline/software/ert/"
    git = "git clone https://bitbucket.org/berkeleylab/cs-roofline-toolkit.git"

    maintainers("kwryankrattiger")

    license("UNKNOWN")

    version("master", branch="master")
    version("v1.1.0", sha256="ef485343c781d5cf94e7cb449baa0c199b291575b71e773c5cf50f7fd685b733")

    variant("mpi", default=True)

    depends_on("cxx", type=("run"))
    depends_on("python@3:", type=("run"))
    depends_on("gnuplot@4.2:", type=("run"))

    depends_on("mpi", type=("run"), when="+mpi")

    def url_for_version(self, version):
        # There are no tags available, so map the version to the git commit hash
        branch_or_commit_hash = version_to_hash_map.get(version)
        return f"https://bitbucket.org/berkeleylab/cs-roofline-toolkit/get/{branch_or_commit_hash}.tar.gz"

    def install(self, spec, prefix):
        ert_dir = "Empirical_Roofline_Tool-1.1.0"
        # ERT by default just installs it's entire self into a directory.
        install(ert_dir, prefix)
