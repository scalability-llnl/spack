# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.store

description = "rebuild Spack's package database"
section = "admin"
level = "long"


def reindex(parser, args):
    spack.store.STORE.reindex()
