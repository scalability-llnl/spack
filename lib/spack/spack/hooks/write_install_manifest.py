# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.verify


def post_install(spec, explicit=None):
    if not spec.external:
        spack.verify.write_manifest(spec)
