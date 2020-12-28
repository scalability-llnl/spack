# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kubernetes(Package):
    """Kubernetes is an open source system for managing containerized
    applications across multiple hosts. It provides basic mechanisms
    for deployment, maintenance, and scaling of applications."""

    homepage = "https://kubernetes.io"
    url      = "https://github.com/kubernetes/kubernetes/archive/v1.19.0-alpha.0.tar.gz"

    version('1.18.1', sha256='33ca738f1f4e6ad453b80f231f71e62470b822f21d44dc5b8121b2964ae8e6f8')
    version('1.18.0', sha256='6bd252b8b5401ad6f1fb34116cd5df59153beced3881b98464862a81c083f7ab')
    version('1.17.4', sha256='b61a6eb3bd5251884f34853cc51aa31c6680e7e476268fe06eb33f3d95294f62')

    depends_on('go', type='build')

    def install(self, spec, prefix):
        make()
        install_tree('_output/bin', prefix.bin)
