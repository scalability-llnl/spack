# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.file_permissions as fp


def post_install(spec, explicit=None):
    if not spec.external:
        fp.set_permissions_by_spec(spec.prefix, spec)

        # os.walk explicitly set not to follow links
        for root, dirs, files in os.walk(spec.prefix, followlinks=False):
            for d in dirs:
                if not os.path.islink(os.path.join(root, d)):
                    fp.set_permissions_by_spec(os.path.join(root, d), spec)
            for f in files:
                if not os.path.islink(os.path.join(root, f)):
                    fp.set_permissions_by_spec(os.path.join(root, f), spec)
