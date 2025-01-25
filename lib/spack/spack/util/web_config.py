# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module breaks the spack.config<->spack.util.web circular import.

Usage: spack.main is expected to instantiate/update the WebConfig instance
after configuration files are processed.
"""

# TODO: Replace NameTuple with dataclass once support only Python @3.7:
# from dataclasses import dataclass
from typing import NamedTuple, Optional

import llnl.util.lang


# TODO: Replace NamedTuple with dataclass once support only Python @3.7:
# TODO: Integrate defaults into WebConfig once allow a dataclass
# @dataclass
class WebConfig(NamedTuple):
    ssl_certs: Optional[str]
    verify_ssl: bool
    connect_timeout: int
    url_fetch_method: str


def _create_global() -> WebConfig:
    default_config = dict()
    return create(default_config)


CONFIG: WebConfig = llnl.util.lang.Singleton(_create_global)  # type: ignore


def update(config: dict) -> WebConfig:
    """Instantiate the configuration by passing spack.config.CONFIG."""
    global CONFIG

    CONFIG = WebConfig(
        ssl_certs=config.get("config:ssl_certs"),
        verify_ssl=config.get("config:verify_ssl", True),
        connect_timeout=config.get("config:connect_timeout", 10),
        url_fetch_method=config.get("config:url_fetch_method", "urllib"),
    )
