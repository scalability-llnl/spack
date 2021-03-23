# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.spec
import spack.store


@pytest.mark.parametrize('hash_length', [1, 2, 3, 4, 5, 9])
@pytest.mark.use_fixtures('mock_packages')
def test_set_install_hash_length(hash_length, mutable_config, tmpdir):
    mutable_config.set('config:install_hash_length', hash_length)
    mutable_config.set('config:install_tree', {'root': str(tmpdir)})
    # The call below is to reinitialize the directory layout associated
    # with the store according to the configuration changes above (i.e.
    # with the shortened hash)
    store = spack.store._store()
    with spack.store.use_store(store):
        spec = spack.spec.Spec('libelf').concretized()
        prefix = spec.prefix
        hash_str = prefix.rsplit('-')[-1]
        assert len(hash_str) == hash_length


@pytest.mark.use_fixtures('mock_packages')
def test_set_install_hash_length_upper_case(mutable_config, tmpdir):
    mutable_config.set('config:install_hash_length', 5)
    mutable_config.set(
        'config:install_tree',
        {
            'root': str(tmpdir),
            'projections': {
                'all': '{name}-{HASH}'
            }
        }
    )
    # The call below is to reinitialize the directory layout associated
    # with the store according to the configuration changes above (i.e.
    # with the shortened hash and projection)
    store = spack.store._store()
    with spack.store.use_store(store):
        spec = spack.spec.Spec('libelf').concretized()
        prefix = spec.prefix
        hash_str = prefix.rsplit('-')[-1]
        assert len(hash_str) == 5
