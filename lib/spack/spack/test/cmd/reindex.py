# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from spack.main import SpackCommand
import spack.store

install = SpackCommand('install')
deprecate = SpackCommand('deprecate')
reindex = SpackCommand('reindex')


def test_reindex_basic(mock_packages, mock_archive, mock_fetch,
                       install_mockery):
    install('libelf@0.8.13')
    install('libelf@0.8.12')

    all_installed = spack.store.store.db.query()

    reindex()

    assert spack.store.store.db.query() == all_installed


def test_reindex_db_deleted(mock_packages, mock_archive, mock_fetch,
                            install_mockery):
    install('libelf@0.8.13')
    install('libelf@0.8.12')

    all_installed = spack.store.store.db.query()

    os.remove(spack.store.store.db._index_path)
    reindex()

    assert spack.store.store.db.query() == all_installed


def test_reindex_with_deprecated_packages(mock_packages, mock_archive,
                                          mock_fetch, install_mockery):
    install('libelf@0.8.13')
    install('libelf@0.8.12')

    deprecate('-y', 'libelf@0.8.12', 'libelf@0.8.13')

    all_installed = spack.store.store.db.query(installed=any)
    non_deprecated = spack.store.store.db.query(installed=True)

    os.remove(spack.store.store.db._index_path)
    reindex()

    assert spack.store.store.db.query(installed=any) == all_installed
    assert spack.store.store.db.query(installed=True) == non_deprecated
