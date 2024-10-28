# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.

import platform

from spack.package import *
from spack.util.prefix import Prefix

# FIXME Remove hack for polymorphic versions
# This package uses a ugly hack to be able to dispatch, given the same
# version, to different binary packages based on the platform that is
# running spack. See #13827 for context.
# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()
_versions = {
    "24.9": {
        "Linux-aarch64": (
            "8d900f798ef806c64993fd4fedf2c2c812dd1ccdbac2a0d33fabcd0cd36f19cf",
            "https://developer.download.nvidia.com/hpc-sdk/24.9/nvhpc_2024_249_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "30c493350cf67481e84cea60a3a869e01fa0bcb71df8e898266273fbdf0a7f26",
            "https://developer.download.nvidia.com/hpc-sdk/24.9/nvhpc_2024_249_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "24.7": {
        "Linux-aarch64": (
            "256ae392ed961162f3f6dc633498db2b68441103a6192f5d4a1c18fa96e992e7",
            "https://developer.download.nvidia.com/hpc-sdk/24.7/nvhpc_2024_247_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "bf2094aa2fc5bdbcbf9bfa0fddc1cbed1bfa6e9342980649db2350d9f675f853",
            "https://developer.download.nvidia.com/hpc-sdk/24.7/nvhpc_2024_247_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "24.5": {
        "Linux-aarch64": (
            "c52b5ba370e053472cbffb825ba1da5b6abaee93d4e15479ec12c32d6ebc47d5",
            "https://developer.download.nvidia.com/hpc-sdk/24.5/nvhpc_2024_245_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "e26c5027ffd83fd9e854946670a97253e950cdbacd4894a6715aea91070042ae",
            "https://developer.download.nvidia.com/hpc-sdk/24.5/nvhpc_2024_245_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "24.3": {
        "Linux-aarch64": (
            "6385847de5f8725e5c56d2abf70c90fed5490f2e71a7bd13d3f4ada8720ef036",
            "https://developer.download.nvidia.com/hpc-sdk/24.3/nvhpc_2024_243_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "a9fe5ec878e9c4cc332de732c6739f97ac064ce76ad3d0af6d282658d27124cb",
            "https://developer.download.nvidia.com/hpc-sdk/24.3/nvhpc_2024_243_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "24.1": {
        "Linux-aarch64": (
            "8c2ce561d5901a03eadce7f07dce5fbc55e8e88c87b74cf60e01e2eca231c41c",
            "https://developer.download.nvidia.com/hpc-sdk/24.1/nvhpc_2024_241_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "e7330eb35e23dcd9b0b3bedc67c0d5443c4fd76b59caa894a76ecb0d17f71f43",
            "https://developer.download.nvidia.com/hpc-sdk/24.1/nvhpc_2024_241_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "27992e5fd56af8738501830daddc5e9510ebd553326fea8730236fee4f0f1dd8",
            "https://developer.download.nvidia.com/hpc-sdk/24.1/nvhpc_2024_241_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "23.11": {
        "Linux-aarch64": (
            "cf744498d1d74ba0af4294388706644ad3669eb0cacea3b69e23739afa2806a0",
            "https://developer.download.nvidia.com/hpc-sdk/23.11/nvhpc_2023_2311_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "b08591438bd0802d4c7c78e7c5bc36383a59591b8c2fa8aed5c4b87b24f7bfbb",
            "https://developer.download.nvidia.com/hpc-sdk/23.11/nvhpc_2023_2311_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "33483a069a911f9309cd53859ab90d2778fb176df906e9e8d2bd55f45eeec400",
            "https://developer.download.nvidia.com/hpc-sdk/23.11/nvhpc_2023_2311_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "23.9": {
        "Linux-aarch64": (
            "dd32ae4233438adb71b2b4f8891f04802fdf90f67036ecf18bfde1b6043a03c3",
            "https://developer.download.nvidia.com/hpc-sdk/23.9/nvhpc_2023_239_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "984d61695499db098fd32be8345c1f7d7c637ea3bdb29cef17aad656f16b000f",
            "https://developer.download.nvidia.com/hpc-sdk/23.9/nvhpc_2023_239_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "ecf343ecad2398e21c8d7f24a580b2932348017dfd8ea38c1ef31b37114b2d4b",
            "https://developer.download.nvidia.com/hpc-sdk/23.9/nvhpc_2023_239_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "23.7": {
        "Linux-aarch64": (
            "d3b9b674045e6e17156b298941be4e1e1e7dea6a3c1938f14ad653b180860ff2",
            "https://developer.download.nvidia.com/hpc-sdk/23.7/nvhpc_2023_237_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "67b137cf67e2c8556ef3952d1ee35f4966c9d1968626825924fb8e4b198a532b",
            "https://developer.download.nvidia.com/hpc-sdk/23.7/nvhpc_2023_237_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "fea91d95ff18bca1ce7afde50371caa02001ade8bed6ddfc5ff70862ccbebece",
            "https://developer.download.nvidia.com/hpc-sdk/23.7/nvhpc_2023_237_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "23.5": {
        "Linux-aarch64": (
            "3af202ad36bbf205b2af56aabe63b971c01b5ec0e82a02effb3c4928f63bc657",
            "https://developer.download.nvidia.com/hpc-sdk/23.5/nvhpc_2023_235_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "65b1f1780175096fa58e98e80fc897c0d563cacce43b3e87ba157f40a8e34877",
            "https://developer.download.nvidia.com/hpc-sdk/23.5/nvhpc_2023_235_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "071d7119006cb1d7ac22cb91338c20133a02d394efe14931dfa6f5d7dfa54c81",
            "https://developer.download.nvidia.com/hpc-sdk/23.5/nvhpc_2023_235_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "23.3": {
        "Linux-aarch64": (
            "48c837de0b1d2dc31c313b19da752d27527e706cb4150c7a6185a4218fc24ef3",
            "https://developer.download.nvidia.com/hpc-sdk/23.3/nvhpc_2023_233_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "0f2b5b2fff8ffed13428c55809841b4abd3dfe61e2b1a866bbe959e4bcd50223",
            "https://developer.download.nvidia.com/hpc-sdk/23.3/nvhpc_2023_233_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "b94d2b4ae5a23c1a0af7d5b07c785f5057850fe3a6ee5ba0aacdde1019af5d12",
            "https://developer.download.nvidia.com/hpc-sdk/23.3/nvhpc_2023_233_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "23.1": {
        "Linux-aarch64": (
            "5b430e03752954ea62ac1c745b1735cfdaa43b2e981a9412c1465ecb0412fff6",
            "https://developer.download.nvidia.com/hpc-sdk/23.1/nvhpc_2023_231_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "81759e7c747bf4f552b75e7657301f76ecc0828b94fe860f81108c6e83e6ad2b",
            "https://developer.download.nvidia.com/hpc-sdk/23.1/nvhpc_2023_231_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "55a064415f6d4ce6a01823ee27ebd266f4fb579679871e7c1a7c054bdc18e9f5",
            "https://developer.download.nvidia.com/hpc-sdk/23.1/nvhpc_2023_231_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "22.11": {
        "Linux-aarch64": (
            "e60e798657c33b06754d33dfd5ab3bea2882d4a9b9476102303edf2bbe3b7a95",
            "https://developer.download.nvidia.com/hpc-sdk/22.11/nvhpc_2022_2211_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "ef800203cf6040b3a5df24f19944b272f62caee8362875bcb394e86dc1de2353",
            "https://developer.download.nvidia.com/hpc-sdk/22.11/nvhpc_2022_2211_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "cb91b3a04368457d5cfe3c0e9c0611591fdc8076b01ea977343fe7db7fdcfa3c",
            "https://developer.download.nvidia.com/hpc-sdk/22.11/nvhpc_2022_2211_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "22.9": {
        "Linux-aarch64": (
            "bc4473f04b49bc9a26f08c17a72360650ddf48a3b6eefacdc525d79c8d730f30",
            "https://developer.download.nvidia.com/hpc-sdk/22.9/nvhpc_2022_229_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "9aac31d36bb09f6653544978021f5b78c272112e7748871566f7e930f5e7475b",
            "https://developer.download.nvidia.com/hpc-sdk/22.9/nvhpc_2022_229_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "aebfeb826ace3dabf9699f72390ca0340f8789a8ef6fe4032e3c7b794f073ea3",
            "https://developer.download.nvidia.com/hpc-sdk/22.9/nvhpc_2022_229_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "22.7": {
        "Linux-aarch64": (
            "2aae3fbfd2d0d2d09448a36166c42311368f5600c7c346f159c280b412fe924a",
            "https://developer.download.nvidia.com/hpc-sdk/22.7/nvhpc_2022_227_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "6dd4fd382c22769e4fa9508714119abd7d1df3dc58c69414a14b0b0dbc34564f",
            "https://developer.download.nvidia.com/hpc-sdk/22.7/nvhpc_2022_227_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "3ce1c346f8bc7e50defb41c545c8907fdc012ff60b27eb8985cf3213f19d863a",
            "https://developer.download.nvidia.com/hpc-sdk/22.7/nvhpc_2022_227_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "22.5": {
        "Linux-aarch64": (
            "ceeee84e6227e973ad1beded6008d330e3790f7c4598b948fa530fedfa830a16",
            "https://developer.download.nvidia.com/hpc-sdk/22.5/nvhpc_2022_225_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "54d1e45664352d0f9f85ab476dd39496dd1b290e0e1221d3bf63afb940dbe16d",
            "https://developer.download.nvidia.com/hpc-sdk/22.5/nvhpc_2022_225_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "7674bcf7a77570fafee5b8299959c9e998a9a10bb27904335cf1a58b71766137",
            "https://developer.download.nvidia.com/hpc-sdk/22.5/nvhpc_2022_225_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "22.3": {
        "Linux-aarch64": (
            "e0ea1cbb726556f6879f4b5dfe17238f8e7680c772368577945a85c0e08328f0",
            "https://developer.download.nvidia.com/hpc-sdk/22.3/nvhpc_2022_223_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "5e80db6010adc85fe799dac961ae69e43fdf18d35243666c96a70ecdb80bd280",
            "https://developer.download.nvidia.com/hpc-sdk/22.3/nvhpc_2022_223_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "bc60a6faf2237bf20550718f71079a714563fa85df62c341cb833f70eb2fe7bb",
            "https://developer.download.nvidia.com/hpc-sdk/22.3/nvhpc_2022_223_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "22.2": {
        "Linux-aarch64": (
            "a8241d1139a768d9a0066d1853748160e4098253024e17e997983884d0d33a19",
            "https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "f84f72423452968d5bbe02e297f188682c4759864a736a72b32acb3433db3a26",
            "https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "8dfb4007d6912b2722946358ac69409592c1f03426d81971ffbcb6fc5fea2cb8",
            "https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "22.1": {
        "Linux-aarch64": (
            "05cfa8c520a34eab01272a261b157d421a9ff7129fca7d859b944ce6a16d2255",
            "https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "9fa9b64fba2c9b287b5800693417d8065c695d18cab0526bad41d9aecc8be2b3",
            "https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "7e4366509ed9031ff271e73327dd3121909902a81ac436307801a5373efaff5e",
            "https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "21.11": {
        "Linux-aarch64": (
            "3b11bcd9cca862fabfce1e7bcaa2050ea12130c7e897f4e7859ba4c155d20720",
            "https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "ac51ed92de4eb5e1bdb064ada5bbace5b89ac732ad6c6473778edfb8d29a6527",
            "https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "d8d8ccd0e558d22bcddd955f2233219c96f7de56aa8e09e7be833e384d32d6aa",
            "https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "21.9": {
        "Linux-aarch64": (
            "52c2c66e30043add4afccedf0ba77daa0000bf42e0db844baa630bb635b91a7d",
            "https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "cff0b55fb782be1982bfeec1d9763b674ddbf84ff2c16b364495299266320289",
            "https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "7de6a6880fd7e59afe0dee51f1fae4d3bff1ca0fb8ee234b24e1f2fdff23ffc9",
            "https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "21.7": {
        "Linux-aarch64": (
            "73eb3513845b59645f118b1e313472f54519dc252d5f5c32a05df2a2a8a19878",
            "https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "37ea23b5a9c696fb3fdb82855643afc4e02aea618102ec801206441f10fc9fba",
            "https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "49d6e23492d131474698cf12971722d42e13a54a4eddec382e66e1053b4ac902",
            "https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "21.5": {
        "Linux-aarch64": (
            "1a1748cd7cf538199d92ab3b1208935fa4a62708ba21125aeadb328ddc7380d4",
            "https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "4674931a5ce28724308cb9cebd546eefa3f0646d3d08adbea28ba5ad27f0c163",
            "https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "21989e52c58a6914743631c8200de1fec7e10b3449c6c1833f3032ee74b85f8e",
            "https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "21.3": {
        "Linux-aarch64": (
            "88e0dbf8fcdd06a2ba06aacf65ae1625b8683688f6593ed3bf8ce129ce1b17b7",
            "https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "08cd0cd6c80d633f107b44f88685ada7f014fbf6eac19ef5ae4a7952cabe4037",
            "https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "391d5604a70f61bdd4ca6a3e4692f6f2391948990c8a35c395b6867341890031",
            "https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "21.2": {
        "Linux-aarch64": (
            "fe19c0232f7c9534f8699b7432483c9cc649f1e92e7f0961d1aa7c54d83297ff",
            "https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "6b69b6e4ebec6a91b9f1627384c50adad79ebdd25dfb20a5f64cf01c3a07f11a",
            "https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "a3e3393040185ae844002fbc6c8eb4ffdfb97ce8b2ce29d796fe7e9a521fdc59",
            "https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "21.1": {
        "Linux-aarch64": (
            "b276e7c0ff78cee837a597d9136cd1d8ded27a9d1fdae1e7d674e2a072a9a6aa",
            "https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "bc236c212097bac6b7d04d627d9cc6b75bb6cd473a0b6a1bf010559ce328a2b0",
            "https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "d529daf46404724ac3f005be4239f2c30e53f5220bb9453f367dccc3a74d6b41",
            "https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "20.11": {
        "Linux-aarch64": (
            "2f26ca45b07b694b8669e4f761760d4f7faa8d032b21e430adee1af0a27032c1",
            "https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_aarch64_cuda_multi.tar.gz",
        ),
        "Linux-ppc64le": (
            "99e5a5437e82f3914e0fe81feb761a5b599a3fe8b31f3c2cac8ae47e8cdc7b0f",
            "https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "c80fc26e5ba586696f7030f03054c1aaca0752a891c7923faf47eb23b66857ec",
            "https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "20.9": {
        "Linux-aarch64": (
            "3bfb3d17f5ee99998bcc30d738e818d3b94b828e2d8da7db48bf152a01e22023",
            "https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_aarch64_cuda_11.0.tar.gz",
        ),
        "Linux-ppc64le": (
            "b2966d4047e1dfd981ce63b333ab9c0acbdc2a6a505fa217456ac9fa3b8e7474",
            "https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "fe665ab611b03846a90bd70ca4e08c1e59ab527364b971ed0304e0ae73c778d8",
            "https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
    "20.7": {
        "Linux-aarch64": (
            "5b83ca1919199ac0aa609309b31c345c5a6453dd3131fddeef9e3ee9059a0e9b",
            "https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_aarch64_cuda_11.0.tar.gz",
        ),
        "Linux-ppc64le": (
            "800ead240bdf61611910b2f6df24ee1d7359377ff3767c923738dd81fcea9312",
            "https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_ppc64le_cuda_multi.tar.gz",
        ),
        "Linux-x86_64": (
            "a5c5c8726d2210f2310a852c6d6e03c9ef8c75e3643e9c94e24909f5e9c2ea7a",
            "https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz",
        ),
    },
}


class Nvhpc(Package, CompilerPackage):
    """The NVIDIA HPC SDK is a comprehensive suite of compilers, libraries
    and tools essential to maximizing developer productivity and the
    performance and portability of HPC applications. The NVIDIA HPC
    SDK C, C++, and Fortran compilers support GPU acceleration of HPC
    modeling and simulation applications with standard C++ and
    Fortran, OpenACC directives, and CUDA. GPU-accelerated math
    libraries maximize performance on common HPC algorithms, and
    optimized communications libraries enable standards-based
    multi-GPU and scalable systems programming. Performance profiling
    and debugging tools simplify porting and optimization of HPC
    applications."""

    homepage = "https://developer.nvidia.com/hpc-sdk"

    maintainers("samcmill")
    tags = ["e4s", "compiler"]

    skip_version_audit = ["platform=darwin", "platform=windows"]

    redistribute(source=False, binary=False)

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("blas", default=True, description="Enable BLAS")
    variant(
        "install_type",
        default="single",
        values=("single", "network"),
        multi=False,
        description="Network installs are for installations shared "
        "by different operating systems",
    )
    variant("lapack", default=True, description="Enable LAPACK")
    variant("mpi", default=False, description="Enable MPI")
    variant(
        "default_cuda", default="default", description="Default CUDA version, for example 11.8"
    )

    provides("blas", when="+blas")
    provides("lapack", when="+lapack")
    provides("mpi", when="+mpi")

    requires("%gcc", msg="nvhpc must be installed with %gcc")

    # For now we only detect compiler components
    # It will require additional work to detect mpi/lapack/blas components
    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["nvc"]
    cxx_names = ["nvc++"]
    fortran_names = ["nvfortran"]
    compiler_version_argument = "--version"
    compiler_version_regex = r"nv[^ ]* (?:[^ ]+ Dev-r)?([0-9.]+)(?:-[0-9]+)?"

    @classmethod
    def determine_variants(cls, exes, version_str):
        # TODO: use other exes to determine default_cuda/install_type/blas/lapack/mpi variants
        return "~blas~lapack~mpi", {"compilers": cls.determine_compiler_paths(exes=exes)}

    def _version_prefix(self):
        return join_path(self.prefix, "Linux_%s" % self.spec.target.family, self.version)

    def setup_build_environment(self, env):
        env.set("NVHPC_SILENT", "true")
        env.set("NVHPC_ACCEPT_EULA", "accept")
        env.set("NVHPC_INSTALL_DIR", self.prefix)
        if self.spec.variants["default_cuda"].value != "default":
            env.set("NVHPC_DEFAULT_CUDA", self.spec.variants["default_cuda"].value)

        if self.spec.variants["install_type"].value == "network":
            local_dir = join_path(self._version_prefix(), "share_objects")
            env.set("NVHPC_INSTALL_TYPE", "network")
            env.set("NVHPC_INSTALL_LOCAL_DIR", local_dir)
        else:
            env.set("NVHPC_INSTALL_TYPE", "single")

    def install(self, spec, prefix):
        compilers_bin = join_path(self._version_prefix(), "compilers", "bin")
        install = Executable("./install")
        makelocalrc = Executable(join_path(compilers_bin, "makelocalrc"))

        makelocalrc_args = [
            "-gcc",
            self.compiler.cc,
            "-gpp",
            self.compiler.cxx,
            "-g77",
            self.compiler.f77,
            "-x",
            compilers_bin,
        ]
        if self.spec.variants["install_type"].value == "network":
            local_dir = join_path(self._version_prefix(), "share_objects")
            makelocalrc_args.extend(["-net", local_dir])

        # Run install script
        install()

        # Update localrc to use Spack gcc
        makelocalrc(*makelocalrc_args)

    def setup_run_environment(self, env):
        prefix = Prefix(
            join_path(self.prefix, "Linux_%s" % self.spec.target.family, self.version, "compilers")
        )

        env.set("CC", join_path(prefix.bin, "nvc"))
        env.set("CXX", join_path(prefix.bin, "nvc++"))
        env.set("F77", join_path(prefix.bin, "nvfortran"))
        env.set("FC", join_path(prefix.bin, "nvfortran"))

        env.prepend_path("PATH", prefix.bin)
        env.prepend_path("LIBRARY_PATH", prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", prefix.lib)
        env.prepend_path("MANPATH", prefix.man)

        if "+mpi" in self.spec:
            mpi_prefix = Prefix(
                join_path(
                    self.prefix,
                    "Linux_%s" % self.spec.target.family,
                    self.version,
                    "comm_libs",
                    "mpi",
                )
            )
            env.prepend_path("PATH", mpi_prefix.bin)
            env.prepend_path("LD_LIBRARY_PATH", mpi_prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = Prefix(
            join_path(self.prefix, "Linux_%s" % self.spec.target.family, self.version, "compilers")
        )

        env.prepend_path("LIBRARY_PATH", prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", prefix.lib)

        if "+mpi" in self.spec:
            mpi_prefix = Prefix(
                join_path(
                    self.prefix,
                    "Linux_%s" % self.spec.target.family,
                    self.version,
                    "comm_libs",
                    "mpi",
                )
            )

            env.prepend_path("LD_LIBRARY_PATH", mpi_prefix.lib)

    def setup_dependent_package(self, module, dependent_spec):
        if "+mpi" in self.spec or self.provides("mpi"):
            mpi_prefix = Prefix(
                join_path(
                    self.prefix,
                    "Linux_%s" % self.spec.target.family,
                    self.version,
                    "comm_libs",
                    "mpi",
                )
            )

            self.spec.mpicc = join_path(mpi_prefix.bin, "mpicc")
            self.spec.mpicxx = join_path(mpi_prefix.bin, "mpicxx")
            self.spec.mpif77 = join_path(mpi_prefix.bin, "mpif77")
            self.spec.mpifc = join_path(mpi_prefix.bin, "mpif90")

    @property
    def libs(self):
        prefix = Prefix(
            join_path(self.prefix, "Linux_%s" % self.spec.target.family, self.version, "compilers")
        )
        libs = []

        if "+blas" in self.spec:
            libs.append("libblas")

        if "+lapack" in self.spec:
            libs.append("liblapack")
            libs.append("libnvf")

        return find_libraries(libs, root=prefix, recursive=True)

    # Avoid binding stub libraries by absolute path
    non_bindable_shared_objects = ["stubs"]
