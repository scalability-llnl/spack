# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRapiserialize(RPackage):
    """R API Serialization

    This package provides other packages with access to the internal R
    serialization code. Access to this code is provided at the C function
    level by using the registration of native function mechanism. Client
    packages simply include a single header file RApiSerializeAPI.h provided
    by this package. This packages builds on the Rhpc package by Junji Nakano
    and Ei-ji Nakama which also includes a (partial) copy of the file
    src/main/serialize.c from R itself. The R Core group is the original
    author of the serialization code made available by this package."""

    homepage = "https://cloud.r-project.org/web/packages/RApiSerialize/index.html"
    url      = "https://cloud.r-project.org/src/contrib/RApiSerialize_0.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RApiSerialize"

    maintainers = ['dorton21']

    version('0.1.0', sha256='324d42c655c27b4647d194bfcd7c675da95c67ea3a74ce99853502022792a23e')
