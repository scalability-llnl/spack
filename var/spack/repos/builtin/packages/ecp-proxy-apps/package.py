# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class EcpProxyApps(BundlePackage):
    """This is a collection of packages that represents the official suite of
    DOE/ECP proxy applications. This is a Spack bundle package that
    installs the ECP proxy application suite.
    """

    tags = ["proxy-app", "ecp-proxy-app"]
    maintainers("rspavel")

    homepage = "https://proxyapps.exascaleproject.org"

    version("4.0")
    version("3.0")
    version("2.1")
    version("2.0")
    version("1.1")
    version("1.0")

    variant("candle", default=False, description="Also build CANDLE Benchmarks")
    variant("ml", default=False, description="Also build Machine Learning Suite")

    # Added as part of ML Suite with 4.0
    depends_on("minigan@1.0.0", when="+ml @4.0:")
    depends_on("cradl@master", when="+ml @4.0:")
    depends_on("cosmoflow-benchmark@master", when="+ml @4.0:")
    depends_on("mlperf-deepcam@master", when="+ml @4.0:")

    # Added with release 4.0
    depends_on("miniamr@1.6.4", when="@4.0:")

    # Added with release 3.0
    depends_on("miniamr@1.4.4", when="@3.0:3.1")
    depends_on("xsbench@19", when="@3.0:")
    depends_on("laghos@3.0", when="@3.0:")

    # Added with release 2.1
    depends_on("amg2013@1.2", when="@2.1:")
    depends_on("miniamr@1.4.3", when="@2.1")

    # Added with release 2.0
    depends_on("ember@1.0.0", when="@2.0:")
    depends_on("miniqmc@0.4.0", when="@2.0:")
    depends_on("minivite@1.0", when="@2.0:")
    depends_on("picsarlite@0.1", when="@2.0:")
    depends_on("thornado-mini@1.0", when="@2.0:")

    depends_on("laghos@2.0", when="@2.0:2.1")
    depends_on("macsio@1.1", when="@2.0:")
    depends_on("sw4lite@1.1", when="@2.0:")
    depends_on("xsbench@18", when="@2.0:2.1")

    # Dependencies for version 2.0
    depends_on("amg2013@1.1", when="@2.0")
    depends_on("miniamr@1.4.1", when="@2.0:2.1")

    # Added with release 1.1
    depends_on("examinimd@1.0", when="@1.1:")

    depends_on("nekbone@17.0", when="@1.0:")
    depends_on("swfft@1.0", when="@1.0:")

    # Dependencies for versions 1.0:1.1
    depends_on("amg2013@1.0", when="@1.0:1.1")
    depends_on("laghos@1.0", when="@1.0:1.1")
    depends_on("macsio@1.0", when="@1.0:1.1")
    depends_on("miniamr@1.4.0", when="@1.0:1.1")
    depends_on("sw4lite@1.0", when="@1.0:1.1")
    depends_on("xsbench@14", when="@1.0:1.1")

    # Removed after release 1.1
    depends_on("minife@2.1.0", when="@1.0:1.1")
    depends_on("minitri@1.0", when="@1.0:1.1")

    # Removed after release 1.0
    depends_on("comd@1.1", when="@1.0")
