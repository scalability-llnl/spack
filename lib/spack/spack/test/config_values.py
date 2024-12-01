# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.spec
import spack.store


@pytest.mark.parametrize("hash_length", [1, 2, 3, 4, 5, 9])
@pytest.mark.usefixtures("mock_packages")
def test_set_install_hash_length(hash_length, mutable_config, tmpdir):
    mutable_config.set("config:install_hash_length", hash_length)
    with spack.store.use_store(str(tmpdir)):
        spec = spack.spec.Spec("libelf").concretized()
        prefix = spec.prefix
        hash_str = prefix.rsplit("-")[-1]
        assert len(hash_str) == hash_length


@pytest.mark.usefixtures("mock_packages")
def test_set_install_hash_length_upper_case(mutable_config, tmpdir):
    mutable_config.set("config:install_hash_length", 5)
    with spack.store.use_store(str(tmpdir), extra_data={"projections": {"all": "{name}-{HASH}"}}):
        spec = spack.spec.Spec("libelf").concretized()
        prefix = spec.prefix
        hash_str = prefix.rsplit("-")[-1]
        assert len(hash_str) == 5
