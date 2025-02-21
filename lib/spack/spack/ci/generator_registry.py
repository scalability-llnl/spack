# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# Holds all known formatters
"""Generators that support writing out pipelines for various CI platforms,
using a common pipeline graph definition.
"""
import spack.error

_generators = {}


def generator(name):
    """Decorator to register a pipeline generator method.
    A generator method should take PipelineDag, SpackCIConfig, and
    PipelineOptions arguments, and should produce a pipeline file.
    """

    def _decorator(generate_method):
        _generators[name] = generate_method
        return generate_method

    return _decorator


def get_generator(name):
    try:
        return _generators[name]
    except KeyError:
        raise UnknownGeneratorException(name)


class UnknownGeneratorException(spack.error.SpackError):
    def __init__(self, generator_name):
        super().__init__(f"No registered generator for {generator_name}")
