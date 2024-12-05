# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Gatk(Package):
    """
    Genome Analysis Toolkit
    Variant Discovery in High-Throughput Sequencing Data
    """

    homepage = "https://gatk.broadinstitute.org/hc/en-us"
    url = "https://github.com/broadinstitute/gatk/releases/download/4.2.2.0/gatk-4.2.2.0.zip"
    list_url = "https://github.com/broadinstitute/gatk/releases"
    maintainers("snehring")

    license("Unlicense")

    version("4.5.0.0", sha256="dc1a4471e8bb566397db9894ca18acbf8f40f3fc312c8fad9a8c5390c218e916")
    version("4.4.0.0", sha256="444600f7b38b46ad0b3606b7d40ce921e0ff1910a50165872f1c73c7c4a1a390")
    version("4.3.0.0", sha256="e2c27229b34c3e22445964adf00639a0909887bbfcc040f6910079177bc6e2dd")
    version("4.2.6.1", sha256="1125cfc862301d437310506c8774d36c3a90d00d52c7b5d6b59dac7241203628")
    version("4.2.2.0", sha256="ddd902441d1874493796566159288e9df178714ac18216ba05092136db1497fd")
    version("4.1.8.1", sha256="42e6de5059232df1ad5785c68c39a53dc1b54afe7bb086d0129f4dc95fb182bc")
    version("4.1.8.0", sha256="3ce1c2a15c44d0cfc9b2c26111f4518c215a5f9314072b4eb61f07ab5d01eef6")
    version("4.1.7.0", sha256="1ed6f7c3194563a16c53b66e64d1b16d3f5e919d057d9e60f0ae6570eb0882e3")
    version("4.1.6.0", sha256="1a8a0256693c0e1fb83d87b6da4bad4a182bfc2a762394650b627a882694c306")
    version("4.1.5.0", sha256="6fc152c2cae0cc54c7c4cfdfd865a64f7054a820f7d02ca2549511af1dd9882b")
    version("4.1.4.1", sha256="21ae694cfc8b7447381ad5ce62ed4af22e53a228b12495bdcca7df0c73b09cea")
    version("4.1.4.0", sha256="ae54a2b938f704e15ea03d1822b4ce80d9a02108dc3a2b482d80b93edae3d492")
    version("4.1.3.0", sha256="56fd4f03b15a8a01eaa4629f62e3ab15e4d4b957c787efd2d5629b2658c3df0a")
    version("4.1.2.0", sha256="ffc5f9b3d4b35772ee5dac3060b59dc657f30e830745160671d84d732c30dc65")
    version("4.1.1.0", sha256="0d997aaf5c633643c07f0e5f74d0e20364a0f1304b04355bc6e073c65fab6554")
    version("4.1.0.0", sha256="148aa061328d922a570d0120d88f27e61e5da877f542206f4d77f2d788b7d21d")
    version("4.0.12.0", sha256="733134303f4961dec589247ff006612b7a94171fab8913c5d44c836aa086865f")
    version("4.0.11.0", sha256="5ee23159be7c65051335ac155444c6a49c4d8e3515d4227646c0686819934536")
    version("4.0.8.1", sha256="e4bb082d8c8826d4f8bc8c2f83811d0e81e5088b99099d3396d284f82fbf28c9")
    version("4.0.4.0", sha256="801bbb181c275cfabc96dc0cb21f3f901634cec11efde9ba9c8b91e2834feef4")
    version(
        "3.8.1",
        sha256="a0829534d2d0ca3ebfbd3b524a9b50427ff238e0db400d6e9e479242d98cbe5c",
        extension="tar.bz2",
        url="https://storage.googleapis.com/gatk-software/package-archive/gatk/GenomeAnalysisTK-3.8-1-0-gf15c1c3ef.tar.bz2",
    )
    version(
        "3.8.0",
        sha256="d1017b851f0cc6442b75ac88dd438e58203fa3ef1d1c38eb280071ae3803b9f1",
        extension="tar.bz2",
        url="https://storage.googleapis.com/gatk-software/package-archive/gatk/GenomeAnalysisTK-3.8-0-ge9d806836.tar.bz2",
    )

    # Make r a variant. According to the gatk docs it is not essential and not
    # tested.
    # https://github.com/broadinstitute/gatk#R
    # Using R to generate plots
    # Certain GATK tools may optionally generate plots using the R installation
    # provided within the conda environment. If you are uninterested in plotting,
    # R is still required by several of the unit tests. Plotting is currently
    # untested and should be viewed as a convenience rather than a primary
    # output.
    variant("r", default=False, description="Use R for plotting")

    depends_on("java@17", type="run", when="@4.4:")
    depends_on("java@8", type="run", when="@:4.3")
    depends_on("python@2.6:2.8,3.6:", type="run", when="@4.0:")
    depends_on("r@3.2:", type="run", when="@4.0: +r")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        # For ver 3.x will install "GenomeAnalysisTK.jar"
        # For ver 4.x will install both "gatk-package-<ver>-local.jar"
        # and "gatk-package-<ver>-spark.jar"
        install("*.jar", prefix.bin)

        # Skip helper script for versions >4.0
        if spec.satisfies("@4.0:"):
            set_executable("gatk")
            install("gatk", prefix.bin)
        else:
            # Set up a helper script to call java on the jar file,
            # explicitly codes the path for java and the jar file.
            script_sh = join_path(os.path.dirname(__file__), "gatk.sh")
            script = join_path(prefix.bin, "gatk")
            install(script_sh, script)
            set_executable(script)

            # Munge the helper script to explicitly point to java and the
            # jar file.
            java = join_path(self.spec["java"].prefix, "bin", "java")
            kwargs = {"ignore_absent": False, "backup": False, "string": False}
            filter_file("^java", java, script, **kwargs)
            filter_file(
                "GenomeAnalysisTK.jar",
                join_path(prefix.bin, "GenomeAnalysisTK.jar"),
                script,
                **kwargs,
            )

    def setup_run_environment(self, env):
        env.prepend_path("GATK", join_path(self.prefix.bin, "GenomeAnalysisTK.jar"))
