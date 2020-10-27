# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tokei(CargoPackage):
    """Tokei is a program that displays statistics about your code. Tokei will
    show the number of files, total lines within those files and code,
    comments, and blanks grouped by language.
    """

    homepage = "https://github.com/xampprocky/tokei"
    crates_io = "tokei"
    git = "https://github.com/xampprocky/tokei.git"

    maintainers = ["AndrewGaspar"]

    version('master', branch='master')
    version('12.0.4', sha256='61fef2813bec8a83ec1c0f7e25a650cd57047b220e1ce8828b6cc752b9cf5ba8')

    # tokei doesn't build with prefer_dynamic at present, so switch default to
    # False
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )

    variant(
        'yaml',
        default=False,
        description='Support YAML output'
    )

    variant(
        'cbor',
        default=False,
        description='Support CBOR output'
    )

    def cargo_features(self):
        features = []

        for feature in ["yaml", "cbor"]:
            if '+{0}'.format(feature) in self.spec:
                features += [feature]

        return features
