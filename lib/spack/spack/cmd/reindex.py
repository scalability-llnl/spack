# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.store

description = "rebuild Spack's package database"
section = "admin"
level = "long"


def reindex(parser, args):
    spack.store.STORE.reindex()
