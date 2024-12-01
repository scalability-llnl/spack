# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEprosimaFastdds(CMakePackage, PythonExtension):
    """eprosima Fast DDS (formerly Fast RTPS) is a C++ implementation of the DDS
    (Data Distribution Service) standard of the OMG (Object Management Group).
    eProsima Fast DDS implements the RTPS (Real Time Publish Subscribe) protocol,
    which provides publisher-subscriber communications over unreliable transports
    such as UDP, as defined and maintained by the Object Management Group (OMG) consortium.
    This is the python interface for eprosima Fast DDS."""

    homepage = "https://www.eprosima.com/"
    url = "https://github.com/eProsima/Fast-DDS-python/archive/v1.2.2.tar.gz"

    license("Apache-2.0")

    version("1.2.2", sha256="78c53739a66544b8c91d0016560c267e11bd7fdaf727b3bfbffd44ae65c93c62")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.15:", type="build")
    extends("python")
    depends_on("py-pytest", type="test")
    depends_on("swig", type=("build"))
    depends_on("eprosima-fastdds")
    depends_on("openssl")

    root_cmakelists_dir = "fastdds_python"
