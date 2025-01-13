# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Used to test correct application of config line scopes in various cases.

The option `config:cache` is supposed to be False, and overridden to True
from the command line.
"""
import multiprocessing as mp

import spack.config
import spack.subprocess_context


def show_config(serialized_state):
    _ = serialized_state.restore()
    result = spack.config.CONFIG.get("config:ccache")
    if result is not True:
        raise RuntimeError(f"Expected config:ccache:true, but got {result}")


if __name__ == "__main__":
    print("Testing spawn")
    ctx = mp.get_context("spawn")
    serialized_state = spack.subprocess_context.PackageInstallContext(None, ctx=ctx)
    p = ctx.Process(target=show_config, args=(serialized_state,))
    p.start()
    p.join()

    print("Testing fork")
    ctx = mp.get_context("fork")
    serialized_state = spack.subprocess_context.PackageInstallContext(None, ctx=ctx)
    p = ctx.Process(target=show_config, args=(serialized_state,))
    p.start()
    p.join()
