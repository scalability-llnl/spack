# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyNemoToolkit(PythonPackage):
    """NeMo (Neural Modules) is a toolkit for creating AI applications built
    around neural modules.
    """

    homepage = "https://github.com/nvidia/nemo"
    pypi = "nemo_toolkit/nemo_toolkit-1.23.0.tar.gz"

    license("Apache-2.0")

    version("1.23.0", sha256="059f69ca1c6598ee40ab6334a70647fb797a5ef6b813a2d62163b20aead8d050")

    depends_on("cxx", type="build")

    # TODO: can support asr once add missing dependency packages
    # variant("asr", default=False, description="Build with speech recognition collections")

    # TODO: can support multimodal once add missing dependency packages
    variant("multimodal", default=False, description="Build with multimodal collections")

    # TODO: can support nlp once add missing dependency packages
    variant("nlp", default=False, description="Build with NLP collections")

    # TODO: can support tts once add missing dependency packages
    variant("tts", default=False, description="Build with speech syntehsis collections ")

    depends_on("py-setuptools@65.5.1:", type="build")

    with default_args(type=("build", "link", "run")):
        # pyproject.toml
        depends_on("python@3.10", when="@1.23:")

    with default_args(type=("build", "run")):
        # base core dependencies in requires.txt (v1.23.0)
        depends_on("py-huggingface-hub")
        depends_on("py-numba")
        depends_on("py-numpy@1.22:")
        depends_on("py-onnx@1.7:")
        depends_on("py-python-dateutil")
        depends_on("py-ruamel-yaml")
        depends_on("py-scikit-learn")
        depends_on("py-tensorboard")
        depends_on("py-text-unidecode")
        depends_on("py-torch")
        depends_on("py-tqdm@4.41:")
        depends_on("py-triton")
        depends_on("py-wget")
        depends_on("py-wrapt")

        # IFF "all" and "arm" and "aarch" not in platform.machine()
        # depends_on("py-nemo-text-processing")

        # requires.txt [core]
        depends_on("py-hydra-core@1.3.1:1.3.2")
        depends_on("py-omegaconf@:2.3")
        depends_on("py-pytorch-lightning@2:2.0.7")
        depends_on("py-torchmetrics@0.11:")
        depends_on("py-transformers@4.36:")
        depends_on("py-wandb")
        depends_on("py-webdataset@0.1.48:0.1.62")

        # TODO: can uncomment once py-youtokentome package is added
        # # requires.txt [common]
        # depends_on("py-datasets")
        # depends_on("py-inflect")
        # depends_on("py-pandas")
        # depends_on("py-sacremoses@0.0.43:")
        # depends_on("py-sentencepiece@:0")
        # depends_on("py-youtokentome@1.0.5:")  # missing
        # depends_on("py-hydra-core@1.3.1:1.3.2")  # see [core]
        # depends_on("py-omegaconf@:2.3")  # see [core]
        # depends_on("py-pytorch-lightning@2:2.0.7")  # see [core]
        # depends_on("py-torchmetrics@0.11:")   # see [core]
        # depends_on("py-transformers@4.36:")   # see [core]
        # depends_on("py-wandb")   # see [core]
        # depends_on("py-webdataset@0.1.48:0.1.62")   # see [core]

    # TODO: can support asr once add missing dependency packages
    # # requires.txt [asr]
    # with when("+asr"):
    #     with default_args(type=("build", "run")):
    #         depends_on("py-braceexpand")
    #         depends_on("py-editdistance")
    #         depends_on("py-g2p-en")   # missing package
    #         depends_on("py-ipywidgets")
    #         depends_on("py-jiwer")  # missing package
    #         depends_on("py-kaldi-python-io")  # missing package
    #         depends_on("py-kaldiio")
    #         depends_on("py-lhotse>=1.20.0")  # missing package
    #         depends_on("py-librosa>=0.10.0")
    #         depends_on("py-marshmallow")
    #         depends_on("py-matplotlib")
    #         depends_on("py-packaging")
    #         depends_on("py-pyannote.core")  # missing
    #         depends_on("py-pyannote.metrics")  # missing
    #         depends_on("py-pydub")
    #         depends_on("py-pyloudnorm")  # missing
    #         depends_on("py-resampy")
    #         depends_on("py-ruamel-yaml")
    #         depends_on("py-scipy>=0.14")
    #         depends_on("py-soundfile")
    #         depends_on("py-sox")
    #         depends_on("py-texterrors")  # missing
    #         # depends_on("py-hydra-core@1.3.1:1.3.2")  # see [core]
    #         # depends_on("py-omegaconf@:2.3")  # see [core]
    #         # depends_on("py-pytorch-lightning@2:2.0.7")  # see [core]
    #         # depends_on("py-torchmetrics@0.11:")   # see [core]
    #         # depends_on("py-transformers@4.36:")   # see [core]
    #         # depends_on("py-wandb")  # see [core]
    #         # depends_on("py-webdataset@0.1.48:0.1.62")   # see [core]
    #         # depends_on("py-datasets")  # see [common]
    #         # depends_on("py-inflect")  # see [common]
    #         # depends_on("py-pandas")  # see [common]
    #         # depends_on("py-sacremoses@0.0.43:")  # see [common]
    #         # depends_on("py-sentencepiece@:0")  # see [common]
    #         # depends_on("py-youtokentome@1.0.5:")  # see [common]  # missing

    # TODO: can support multimodal once add missing dependency packages
    # with when("+multimodal"):
    #     with default_args(type=("build", "run")):
    #         depends_on("py-addict")
    #         depends_on("py-clip")  # missing
    #         depends_on("py-diffusers@0.19.3":")  # missing
    #         depends_on("py-einops_exts")  # missing
    #         depends_on("py-imageio")
    #         depends_on("py-kornia")
    #         depends_on("py-nerfacc@0.5.3:")  # missing
    #         depends_on("py-open_clip_torch")  # missing
    #         depends_on("py-PyMCubes")  # missing?
    #         depends_on("py-taming-transformers")  # missing
    #         depends_on("py-torchdiffeq")
    #         depends_on("py-torchsde")  # missing
    #         depends_on("py-trimesh")
    #         depends_on("py-boto3")
    #         depends_on("py-einops")
    #         depends_on("py-faiss-cpu")  # missing
    #         depends_on("py-fasttext")  # missing py-
    #         depends_on("py-flask_restful")
    #         depends_on("py-ftfy")
    #         depends_on("py-gdown")
    #         depends_on("py-h5py")
    #         depends_on("py-ijson")  # missing
    #         depends_on("py-jieba")  # missing
    #         depends_on("py-markdown2")
    #         depends_on("py-matplotlib@3.3.2:")
    #         depends_on("py-megatron_core@=0.5.0")  # missing
    #         depends_on("py-nltk@3.6.5:")
    #         depends_on("py-opencc@:1.1.6")  # missing
    #         depends_on("py-pangu")  # missing
    #         depends_on("py-rapidfuzz")
    #         depends_on("py-rouge_score")  # missing
    #         depends_on("py-sacrebleu")
    #         depends_on("py-sentence_transformers")  # missing
    #         depends_on("py-tensorstore@:0.1.45")
    #         depends_on("py-zarr")
    #         # depends_on("py-hydra-core@1.3.1:1.3.2")  # see [core]
    #         # depends_on("py-omegaconf@:2.3")  # see [core]
    #         # depends_on("py-pytorch-lightning@2:2.0.7")  # see [core]
    #         # depends_on("py-torchmetrics@0.11:")   # see [core]
    #         # depends_on("py-transformers@4.36:")   # see [core]
    #         # depends_on("py-wandb")  # see [core]
    #         # depends_on("py-webdataset@0.1.48:0.1.62")   # see [core]
    #         # depends_on("py-datasets")  # see [common]
    #         # depends_on("py-inflect")  # see [common]
    #         # depends_on("py-pandas")  # see [common]
    #         # depends_on("py-sacremoses@0.0.43:")  # see [common]
    #         # depends_on("py-sentencepiece@:0")  # see [common]
    #         # depends_on("py-youtokentome@1.0.5:")  # see [common]  # missing

    # TODO: can support nlp once add missing dependency packages
    # with when("+nlp"):
    #     with default_args(type=("build", "run")):
    #         # depends_on("py-boto3")  # missing
    #         # depends_on("py-einops")
    #         # depends_on("py-faiss-cpu")  # missing
    #         # depends_on("py-"fasttext")  # missing
    #         # depends_on("py-flask_restful")  # missing
    #         # depends_on("py-ftfy")
    #         # depends_on("py-gdown")
    #         # depends_on("py-h5py")
    #         # depends_on("py-ijson")
    #         # depends_on("py-jieba")  # missing
    #         # depends_on("py-markdown2")
    #         # depends_on("py-matplotlib>=3.3.2")
    #         # depends_on("py-megatron_core==0.5.0")  # missing
    #         # depends_on("py-nltk>=3.6.5")
    #         # depends_on("py-opencc<1.1.7")  # missing
    #         # depends_on("py-pangu")  # missing
    #         # depends_on("py-rapidfuzz")
    #         # depends_on("py-rouge_score")  # missing
    #         # depends_on("py-sacrebleu")
    #         # depends_on("py-sentence_transformers")  # missing
    #         # depends_on("py-tensorstore<0.1.46")
    #         # depends_on("py-zarr")
    #         # depends_on("py-hydra-core@1.3.1:1.3.2")  # see [core]
    #         # depends_on("py-omegaconf@:2.3")  # see [core]
    #         # depends_on("py-pytorch-lightning@2:2.0.7")  # see [core]
    #         # depends_on("py-torchmetrics@0.11:")   # see [core]
    #         # depends_on("py-transformers@4.36:")   # see [core]
    #         # depends_on("py-wandb")  # see [core]
    #         # depends_on("py-webdataset@0.1.48:0.1.62")   # see [core]
    #         # depends_on("py-datasets")  # see [common]
    #         # depends_on("py-inflect")  # see [common]
    #         # depends_on("py-pandas")  # see [common]
    #         # depends_on("py-sacremoses@0.0.43:")  # see [common]
    #         # depends_on("py-sentencepiece@:0")  # see [common]
    #         # depends_on("py-youtokentome@1.0.5:")  # see [common]  # missing

    # TODO: can support tts once add missing dependency packages
    # with when("+tts"):
    #     with default_args(type=("build", "run")):
    #         depends_on("py-attrdict")  # missing
    #         depends_on("py-einops")
    #         depends_on("py-jieba")  # missing
    #         depends_on("py-kornia")
    #         depends_on("py-librosa")
    #         depends_on("py-matplotlib")
    #         depends_on("py-nltk")
    #         # depends_on("py-pandas")  # see [common]
    #         depends_on("py-pypinyin")
    #         depends_on("py-pypinyin-dict")  # missing
    #         # depends_on("py-hydra-core@1.3.1:1.3.2")  # see [core]
    #         # depends_on("py-omegaconf@:2.3")  # see [core]
    #         # depends_on("py-pytorch-lightning@2:2.0.7")  # see [core]
    #         # depends_on("py-torchmetrics@0.11:")   # see [core]
    #         # depends_on("py-transformers@4.36:")   # see [core]
    #         # depends_on("py-wandb")  # see [core]
    #         # depends_on("py-webdataset@0.1.48:0.1.62")   # see [core]
    #         # depends_on("py-datasets")  # see [common]
    #         # depends_on("py-inflect")  # see [common]
    #         # depends_on("py-sacremoses@0.0.43:")  # see [common]
    #         # depends_on("py-sentencepiece@:0")  # see [common]
    #         # depends_on("py-youtokentome@1.0.5:")  # see [common]  # missing
    #         depends_on("py-braceexpand")
    #         depends_on("py-editdistance")
    #         depends_on("py-g2p-en")  # missing
    #         depends_on("py-ipywidgets")
    #         depends_on("py-jiwer")  # missing
    #         depends_on("py-kaldi-python-io")  # missing
    #         depends_on("py-kaldiio")
    #         depends_on("py-lhotse>=1.20.0")  # missing
    #         depends_on("py-librosa>=0.10.0")
    #         depends_on("py-marshmallow")
    #         depends_on("py-packaging")
    #         depends_on("py-pyannote.core")  # missing
    #         depends_on("py-pyannote.metrics")  # missing
    #         depends_on("py-pydub")
    #         depends_on("py-pyloudnorm")  # missing
    #         depends_on("py-resampy")
    #         depends_on("py-ruamel-yaml")
    #         depends_on("py-scipy>=0.14")
    #         depends_on("py-soundfile")
    #         depends_on("py-sox")  # missing py-
    #         depends_on("py-texterrors")  # missing
