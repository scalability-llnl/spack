# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmodbus(AutotoolsPackage):
    """libmodbus is a free software library to send/receive data
    according to the Modbus protocol.This library is written in C
    and supports RTU (serial) and TCP (Ethernet) communications."""

    homepage = "https://libmodbus.org/"
    url = "https://github.com/stephane/libmodbus/releases/download/v3.1.10/libmodbus-3.1.10.tar.gz"

    license("LGPL-2.1-or-later")

    version("3.1.10", sha256="899be4e25ab7fe5799d43f9567510d6f063d2e8f56136dd726b6fd976f9b2253")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-0367
        version("3.1.6", sha256="d7d9fa94a16edb094e5fdf5d87ae17a0dc3f3e3d687fead81835d9572cf87c16")
        version("3.1.5", sha256="f7a9538f23a8786b1ee62a4b75879b5c0e194e728350de1b741ce7d595970f06")
        version("3.1.4", sha256="c8c862b0e9a7ba699a49bc98f62bdffdfafd53a5716c0e162696b4bf108d3637")
        version("3.1.3", sha256="9e02d79d715522e03b61c313c7278fcf80860816718587819318b8ad9c3fd0ce")
        version("3.1.2", sha256="661e14f9dc904f3f1b034464ddaa5fd4b8472f8f5d1ea10a1148af85591b7ee9")
        version("3.1.1", sha256="76d93aff749d6029f81dcf1fb3fd6abe10c9b48d376f3a03a4f41c5197c95c99")
        version("3.0.8", sha256="022f0691d920b8aee3ee49d7af0f69b7ef80fc3c849a8e0281d5bc27db7a24ea")
        version("3.0.7", sha256="6c26850cd5dedcf5dad40977ac7f2ee990a3667f6959a1e05e22959bdf537961")
        version("3.0.6", sha256="046d63f10f755e2160dc56ef681e5f5ad3862a57c1955fd82e0ce036b69471b6")
        version("3.0.5", sha256="19aad5d55fa315602d6e836a858a3802f1608f9d824afba05fa12a58a1b1e656")

    depends_on("c", type="build")  # generated
