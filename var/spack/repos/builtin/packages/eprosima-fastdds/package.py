# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EprosimaFastdds(CMakePackage):
    """eprosima Fast DDS (formerly Fast RTPS) is a C++ implementation of the DDS
    (Data Distribution Service) standard of the OMG (Object Management Group).
    eProsima Fast DDS implements the RTPS (Real Time Publish Subscribe) protocol,
    which provides publisher-subscriber communications over unreliable transports
    such as UDP, as defined and maintained by the Object Management Group (OMG) consortium."""

    homepage = "https://www.eprosima.com/"
    url = "https://github.com/eProsima/Fast-DDS/archive/v2.10.1.tar.gz"

    license("Apache-2.0")

    version("2.10.1", sha256="2cc2682db5dc7e87684b7f23166e2f32faf8d5c4b4a8c94c6c21211a8a38f553")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("asio")
    depends_on("tinyxml2")
    depends_on("openssl")
    depends_on("foonathan-memory")
    depends_on("eprosima-fastcdr")
