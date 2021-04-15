# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack
import spack.store
import spack.filesystem_view as fs_view


def pre_uninstall(spec):
    pkg = spec.package
    assert spec.concrete

    if pkg.is_extension:
        target = pkg.extendee_spec.prefix
        view = fs_view.YamlFilesystemView(target, spack.store.store.layout)

        if pkg.is_activated(view):
            # deactivate globally
            pkg.do_deactivate(force=True)
