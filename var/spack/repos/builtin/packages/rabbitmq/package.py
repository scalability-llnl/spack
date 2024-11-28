# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rabbitmq(Package):
    """
    RabbitMQ is lightweight and easy to deploy on premises and in the cloud.
    It supports multiple messaging protocols. RabbitMQ can be deployed in
    distributed and federated configurations to meet high-scale,
    high-availability requirements.
    """

    homepage = "https://www.rabbitmq.com/"
    url = "https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.15/rabbitmq-server-generic-unix-3.6.15.tar.xz"

    license("BSD-2-Clause")

    version("3.6.15", sha256="04e6a291642f80e87fc892d5e8ea309fb3fab85ebb64a79a70dfe6c6cfde36fb")

    def install(self, spec, prefix):
        install_tree(".", prefix)
