# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ArmForge(Package):
    """Arm Forge is the complete toolsuite for software development - with
    everything needed to debug, profile, optimize, edit and build C, C++ and
    Fortran applications on Linux for high performance - from single threads
    through to complex parallel HPC codes with MPI, OpenMP, threads or CUDA."""

    homepage = "http://www.allinea.com/products/develop-allinea-forge"

    # TODO: this mess should be fixed as soon as a way to parametrize/constrain
    #       versions (and checksums) based on the target platform shows up

    version(
        "19.0.4-Redhat-6.0-x86_64",
        sha256="0b0b6ed5c3d6833bad46d5ea84346cd46f0e4b3020c31f2fd4318b75ddaf01aa",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Redhat-6.0-x86_64.tar",
    )
    version(
        "19.0.4-Redhat-7.0-x86_64",
        sha256="de3c669f7cb4daf274aae603294c416a953fb558e101eb03bcccf0ef4291e079",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Redhat-7.0-x86_64.tar",
    )
    version(
        "19.0.4-Suse-11-x86_64",
        sha256="24a2c7761c2163f128e4f4b60e963c53774196809ddfa880131c5dde5eb454c2",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Suse-11-x86_64.tar",
    )
    version(
        "19.0.4-Suse-12-x86_64",
        sha256="6688192291fe9696922a34371d07ea66f89bff9b976fd99796e5f9a6651f86e6",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Suse-12-x86_64.tar",
    )
    version(
        "19.0.4-Suse-15-x86_64",
        sha256="dea60d93a157ab6952fd6887f40123ab9d633d5589ffe7824d53fb269294cf35",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Suse-15-x86_64.tar",
    )
    version(
        "19.0.4-19.0.4-Ubuntu-16.04-x86_64",
        sha256="240741beff96f6a0b3976bc98d90863fe475366d5c093af9b96b877a230d479c",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Ubuntu-16.04-x86_64.tar",
    )
    version(
        "19.0.4-Ubuntu-14.04-x86_64",
        sha256="135903906111b61045ddd3e98f1d8e8fd02b5b6ef554a68dfbe6760c76ec65a2",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Ubuntu-14.04-x86_64.tar",
    )
    version(
        "19.0.4-Redhat-7.2-ppc64le",
        sha256="73cb9f4005278e8dd2106a871dcbb53edb8855faeeda75c7abd7936f85fcce56",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Redhat-7.2-ppc64le.tar",
    )
    version(
        "19.0.4-Redhat-7.4-aarch64",
        sha256="8d168e5665a158f65b72d7b996fd283f7f538efbff15648eff44cfb7371ecad7",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Redhat-7.4-aarch64.tar",
    )
    version(
        "19.0.4-Suse-12-aarch64",
        sha256="de3aa62c5b5d5181a7947dcd1dfa66df5d06fd482394044100147210c8182d75",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Suse-12-aarch64.tar",
    )
    version(
        "19.0.4-Ubuntu-16.04-aarch64",
        sha256="3910e320c635dd5c09af7f5696909c7c0ae25406910d2e592e522ed0233e0451",
        url="http://content.allinea.com/downloads/arm-forge-19.0.4-Ubuntu-16.04-aarch64.tar",
    )
    version(
        "19.0.3-Redhat-6.0-x86_64",
        sha256="0ace88a1847d8f622f077cd38fa9dddf7f2d6dd6aad086be0e0a66e10fb8b64b",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Redhat-6.0-x86_64.tar",
    )
    version(
        "19.0.3-Redhat-7.0-x86_64",
        sha256="35c7a9532aa19251343c37b8f5eb51ef04f7b6e8b42bea2bd932f4d83a1e8375",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Redhat-7.0-x86_64.tar",
    )
    version(
        "19.0.3-Suse-11-x86_64",
        sha256="48fe2b1b81a824909fedf5e02cd08d8a62033cce80440eca6efbea0ae8023e75",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Suse-11-x86_64.tar",
    )
    version(
        "19.0.3-Suse-12-x86_64",
        sha256="b4d0f91780dc43544ea946f5117a50ba18750fd50ef811cae5b6b6771b4ebb77",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Suse-12-x86_64.tar",
    )
    version(
        "19.0.3-Ubuntu-16.04-x86_64",
        sha256="ed6726434a6d24d413ed6183756433d63438936dc671cb6a3567b407c8e233e1",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Ubuntu-16.04-x86_64.tar",
    )
    version(
        "19.0.3-Ubuntu-14.04-x86_64",
        sha256="22350d068c4ef60d1aad330636d443f00269c0cc49bed4c05b80f93b9d9a9c66",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Ubuntu-14.04-x86_64.tar",
    )
    version(
        "19.0.3-Redhat-7.2-ppc64le",
        sha256="dc6ea53eead78f0d9ffd8fa74ffddb80e8bd3b4ab8a1edd6f8505ffbea9cea15",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Redhat-7.2-ppc64le.tar",
    )
    version(
        "19.0.3-Redhat-7.4-aarch64",
        sha256="4e19d4200e2936d542bf2b9dc79c7f8b00ccfb37b9191dfc90ac0787680a8b0c",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Redhat-7.4-aarch64.tar",
    )
    version(
        "19.0.3-Suse-12-aarch64",
        sha256="9b27b678d0228b4e51fd517ef0acd1df65b780a3a0b226caa6b6f1b7dccf31e6",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Suse-12-aarch64.tar",
    )
    version(
        "19.0.3-Ubuntu-16.04-aarch64",
        sha256="4470f7067d4a4e0369df8af28b6ca95f58fa0062bf8dffc49f0b7415112c0332",
        url="http://content.allinea.com/downloads/arm-forge-19.0.3-Ubuntu-16.04-aarch64.tar",
    )

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["licences/Licence"]
    license_vars = [
        "ALLINEA_LICENSE_DIR",
        "ALLINEA_LICENCE_DIR",
        "ALLINEA_LICENSE_FILE",
        "ALLINEA_LICENCE_FILE",
    ]
    license_url = "http://www.allinea.com/user-guide/forge/Installation.html"

    def install(self, spec, prefix):
        os.system("./textinstall.sh --accept-licence " + prefix)
