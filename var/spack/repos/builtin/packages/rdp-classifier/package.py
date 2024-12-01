# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RdpClassifier(Package, SourceforgePackage):
    """The RDP Classifier is a naive Bayesian classifier that can rapidly and
    accurately provides taxonomic assignments from domain to genus, with
    confidence estimates for each assignment."""

    homepage = "http://rdp.cme.msu.edu/"
    sourceforge_mirror_path = "rdp-classifier/rdp_classifier_2.12.zip"

    license("GPL-2.0-only")

    version("2.12", sha256="977896248189a1ce2146dd3a61d203c3c6bc9aa3982c60332d463832922f7d0a")

    depends_on("java", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path("dist", "classifier.jar"), prefix.bin)
        install_tree(join_path("dist", "lib"), prefix.bin.lib)
        install(join_path("lib", "junit-4.8.2.jar"), prefix.bin.lib)
        install_tree("src", prefix.src)
