# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.config
import spack.main


def pre_uninstall(spec):
    """unregister extensions from configs"""
    # this conditional can be on package type later
    if hasattr(spec.package, "spack_extension"):
        config = spack.main.SpackCommand("config")
        extension_path = os.path.join(spec.prefix, spec.name)
        for scope in spec.variants["scopes"].value:
            if scope != "none":
                rm_args = ["--scope", scope]
                rm_args.extend(["rm", "config:extensions:[{0}]".format(extension_path)])
                config(*rm_args)
