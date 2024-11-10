# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.compilers.xl

#: compiler symlink mappings for mixed f90/fc compilers
fc_mapping = [("xlf2008_r", os.path.join("xl", "xlf2008_r"))]


class XlR(spack.compilers.xl.Xl):
    # Named wrapper links within build_env_path
    @property
    def link_paths(self):
        link_paths = {
            "cc": os.path.join("xl_r", "xlc_r"),
            "cxx": os.path.join("xl_r", "xlc++_r"),
            "f77": os.path.join("xl_r", "xlf_r"),
        }

        # fortran links need to look at the actual compiler names from
        # compilers.yaml to figure out which named symlink to use
        for compiler_name, link_path in fc_mapping:
            if self.fc and compiler_name in self.fc:
                link_paths["fc"] = link_path
                break
        else:
            link_paths["fc"] = os.path.join("xl", "xlf90_r")

        return link_paths
