# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpressio(CMakePackage, CudaPackage):
    """A generic abstraction for the compression of dense tensors"""

    # codarcode gets "stable" releases ~1/yr; robertu94 contains development versions
    homepage = "https://github.com/codarcode/libpressio"
    url = "https://github.com/robertu94/libpressio/archive/0.31.1.tar.gz"
    git = "https://github.com/robertu94/libpressio"

    tags = ["e4s"]
    maintainers("robertu94")

    tests_require_compiler = True
    version("master", branch="master")
    version("develop", branch="develop")
    version("0.99.4", sha256="091e4bac2cedca5fb9495a22eee7be718c2d04d899d56c65fc088936884eac0e")
    version("0.99.2", sha256="556d157097b2168fefde1fe3b5e2da06a952346357d46c55548d92c77d1da878")
    version("0.99.1", sha256="c9b19deaac4df5eaeecd938fea4c1752d86474f453880c0ba984ceee6bf15d35")
    version("0.99.0", sha256="b95916c4851a7ec952e5f29284e4f7477eaeff0e52a2e5b593481c72edf733d6")
    version("0.98.1", sha256="5246271fdf2e4ba99eeadfccd6224b75bf3af278a812ded74ec9adc11f6cabba")
    version("0.98.0", sha256="6b6507bf1489ff2cbeaf4c507d34e1015495c811730aa809e778f111213062db")
    version("0.97.3", sha256="631111253ec4cfd3138773eaf8280921e220b0d260985da762f0a0152e5b1b17")
    version("0.97.2", sha256="70d549ef457d5192c084fbf6304cb362d367786afe88d7b8db4eea263f9c7d43")
    version("0.96.6", sha256="a8d3269f0f5289d46471a5b85e5cd32e370edb8df45d04f5e707e0a1f64eccd8")
    version("0.96.5", sha256="7cca6f3f98dde2dbd1c9ff7462d09975f6a3630704bd01b6bef6163418a0521b")
    version("0.96.4", sha256="7f012b01ce1a6c9f5897487089266de5b60659ed6b220eadba51d63613620404")
    version("0.96.3", sha256="e8f4af028d34df2f3c8eb61cfc2f93fadab7a2e2d072a30ee6a085fb344a3be4")
    version("0.96.2", sha256="2c904ec16900b67ab0188ea96d27fa4efca2c9efc1b214119451becaaeaa2d18")
    version("0.96.1", sha256="2305d04b57c1b49ecd5a4bda117f1252a57529c98e6bd260bfe5166a4f4d4043")
    version("0.96.0", sha256="42f563b70c4f77abffb430284f0c5bc9adba2666412ee4072d6f97da88f0c1a0")
    version("0.95.1", sha256="c2e4f81d1491781cd47f2baba64acfbba9a7d6203c9b01369f8b1a8f94e0bb2b")
    version("0.94.0", sha256="4250597cdd54043a7d5009ffc3feea3eac9496cdd38ea3f61f9727b7acd09add")
    version("0.93.0", sha256="1da5940aaf0190a810988dcd8f415b9c8db53bbbdfcb627d899921c89170d990")
    version("0.92.0", sha256="e9cab155deb07aabdca4ece2c826be905ed33f16c95f82f24eb01d181fce6109")
    version("0.91.1", sha256="35cd4b93e410a83c626c9c168d59ade3bf26a453bcbf50dfd77b6d141184b97c")
    version("0.91.0", sha256="6220988dc964c36cdffdbc5e055261ac7a0189ad80b67a962189683648209d2e")
    version("0.90.2", sha256="1fe3f4073952a96bda1b3d7c237bc5d64d1f7bf13bfe1830074852ea33006bf9")
    version("0.88.3", sha256="b2df2ed11f77eb2e07206f7bdfa4754017559017235c3324820021ef451fd48b")
    version("0.88.2", sha256="f5de6aff5ff906b164d6b2199ada10a8e32fb1e2a6295da3f0b79d9626661a46")
    version("0.88.1", sha256="d7fe73a6b2d8de6d19c85e87888dcf1a62956f56b4e6dfd23e26901740031e00")
    version("0.88.0", sha256="4358441f0d10559d571327162a216617d16d09569a80e13ad286e3b7c41c5b9b")
    version("0.87.0", sha256="2bea685e5ed3a1528ea68ba4a281902ff77c0bebd38ff212b6e8edbfa263b572")
    version("0.86.7", sha256="2a6319640a018c39aa93aaf0f027fd496d7ea7dc5ac95509313cf1b4b6b1fb00")
    version("0.86.6", sha256="31ac77137c31a524c2086e1fe4d9b1d3c1bc6d8594662cd4b67878ba8887cabb")
    version("0.86.5", sha256="6e6ffe7585e298061f6f5ff79a9fe7edf722a8c124a87282bae864ed6a167246")
    version("0.86.4", sha256="52a1d932b30a9390e836ea4b102225b176f8feebbac598a0ab3a81a9ac83775c")
    version("0.86.3", sha256="6b010e394fc916ad2233e941a49f70555dda40521e3668f2e10502c7bfa529be")
    version("0.86.2", sha256="e221cb256e1b387ce1245cab5704c10d351812c003b257655d43b156b9650a89")
    version("0.86.1", sha256="89b1b652215f67635da1baac81d3f927ff00f335c473322edcf24472b5a9b5a4")
    version("0.86.0", sha256="867bd6ea6b632b7f6d6a89aac073cea738b574825c81ee83318802e9d3d5fbe8")
    version("0.85.0", sha256="79a600fdd5c7a418a0380425e1bbeb245d5d86e1676f251e5900b69738b72423")
    version("0.84.3", sha256="7b2ca198f919c1f981c88722da33ef69b564fe123d49330ad6ba17eba80c046e")
    version("0.84.2", sha256="c50b599a22ab89b7ef57dbaa717f5e97f4437d2bd4b6e572274c8c98022b05da")
    version("0.84.0", sha256="b22320a54dbb9f65a66af2a6f335884e7ba48abd3effe643e51e4e7cfe793b7d")
    version("0.83.4", sha256="9dd0efff1c6121e964b45371d6a52895f6a8db3d5cdabbd1e951b696a3f590e3")
    version("0.83.3", sha256="59e2bb2c1eb422c03204bfc713bc76d7bbaeaeba6430e1204577495c07eef34d")
    version("0.83.2", sha256="56dd63cb3924fb57f8f53929faecf2a5211985f160cdacf38b3d001e22728427")
    version("0.83.1", sha256="2afdc8421b4c0f638c8547bcdd54bdb405d1717dca32b804621c5c152adbe2a6")
    version("0.83.0", sha256="7c692bbf3ebdfa508a493902eb561c85b9087dd8003547dcd54baf0b2188d9bd")
    version("0.82.3", sha256="97a6a0a022d8ae60f477ce21d1ff10cc47bb2f7d3891bb3b49f4a7b166f9c2e1")
    version("0.82.2", sha256="ce2d566c627a5341e1fd58261b2d38567b84d963f1045e2e4aac87e67ac06d89")
    version("0.82.1", sha256="f6b41ad6f56311078e67e68063f9124f32e63a9c1c9c0c0289c75addaf9fed94")
    version("0.82.0", sha256="e60f843dda8312ae4269c3ee23aad67b50f29a8830c84fb6c10309c37e442410")
    version("0.81.0", sha256="51ab443a42895fefb4e0ae8eb841402f01a340f3dd30dcb372f837e36ac65070")
    version("0.80.1", sha256="9168789f8714d0bbce1a03ff3a41ef24c203f807fed1fbd5ca050798ebef015f")
    version("0.80.0", sha256="f93292dc258224a8ef69f33299a5deecfb45e7ea530575eeaa4ceff48093d20e")
    version("0.79.0", sha256="e843d8f70369e30d0135b513926ac4a5dacd3042c307c132e80a29b7349e8501")
    version("0.78.0", sha256="d9292150686d2be616cd9145c24fe6fc12374df023eee14099ffdf7071e87044")
    version("0.77.0", sha256="d2f362c8b48b6ea6b3a099f3dcb0ce844e3b45fd6cf0c4130fbbf48d54d1a9b3")
    version("0.76.1", sha256="09b6926efefa1b10f400dfc94927c195d1f266f34ed34cddeba11707c0cc6982")
    version("0.76.0", sha256="8ec0e3bcc57511a426047748f649096cf899a07767ddbcdbfad28500e1190810")
    version("0.75.1", sha256="8b9beb79507196575649d32116d13833e7dc9765370c245ac5a3640a50cb106a")
    version("0.75.0", sha256="83aadd5e6172b3654b955954d13f2d9346fcd008bc901746f6f8b65a978235ee")
    version("0.74.1", sha256="aab7211c244a7a640e0b2d12346463c8650ef4f8d48fc58819a20d3b27ab5f81")
    version("0.74.0", sha256="2fbd54bbc4d1f3ce4b107ac625ad97c6396bff8873f2ac51dd049d93aa3f2276")
    version("0.73.0", sha256="059c90ab50d2e50a1fff8bf25c0c387a9274090bf8657fa49aa1c211b4690491")
    version("0.72.2", sha256="1f620b8af272dd2823712c1e38a69c6375febe49eb9155a3f04667ea1931ebdb")
    version("0.72.1", sha256="f8ab9559c40a6a93ad0c1a894acf71e07c9fe1994f464852c9dd6f0423a6dc51")
    version("0.72.0", sha256="0e6e7327a21a0cd6cf56fa4c62ba5ec1c41381ac053602d8acaa854bdfd1cb30")
    version("0.71.3", sha256="f1185acdc6143fe7e417754032336ef50fec5760b08cb291962305429adf18da")
    version("0.71.2", sha256="0501f6a0a9cfad62f80834d1dd77c678b000202903168aec0d2c4928ff6e581c")
    version("0.71.1", sha256="cd9daa4b28da3b5e3cb36cace11b4e580a66fb14ca04a807c5a135a9448bb5df")
    version("0.71.0", sha256="9b9ba9689c53e9cfa4d9fee52653ed393d2307c437dac41daceb6f98564fbcd1")
    version("0.70.8", sha256="f0600cabd0341669ef1d6e838ef3496cff5200239a3b96a4941c434d71e4517c")
    version("0.70.7", sha256="82722a9e7fbec3b2d79be226ba73bbf3108d3206d006a763db46d20cc044a8b5")
    version("0.70.6", sha256="e76be47b0b8bd18d7ac44d59242adc45dc721465638aefd2c8564fd778d1adbd")
    version("0.70.5", sha256="c6ee62643c08a7ceca7c45eb28edff0eeb070671bf0d502563b6cc8ada4bf695")
    version("0.70.4", sha256="6df62154d0a8919fa91f6fce4ffb2f77584d5ddc61c85eee34557d36de9906b2")
    version("0.70.3", sha256="40cca7f6d3bd19fdcf6f6c17521acdf63dfda0fb5b173c23d4521818b16a9a46")
    version("0.70.2", sha256="30929e02c0ce5db8d9ff1eeca42df92e68439c7dd5a3c1fea0bb44ead2343442")
    version("0.70.1", sha256="855923ca58b1c549681d368d2112d05b96fae9e3199f2a10c2013fcb2f630036")
    version("0.70.0", sha256="1e987dcea76b2bd01f7e59b404267c7614a7c99b3fbc0ae745bf8e9426f489c6")
    version("0.69.0", sha256="22e47deb4791778846b9c858295b756f91e1d8c884ccf246c2df2bf9b56a04d5")
    version("0.68.0", sha256="c7008e6f6b4451812070ece7e9b2fb6cc2fb04971255f95c8274375a698c6794")
    version("0.66.3", sha256="7423339831525a128115d446b1dd7fb7942f2aed24e0ec3778396d2c0c379678")
    version("0.66.2", sha256="89a6459b6fcf1273f8afc7317e7351c09be977aeb3bb6554941166074ee2030f")
    version("0.66.1", sha256="1de2d3d911fc91f7aa9f57eda467f1aadd7060a680538b82c678a5f4e7e6c5d0")
    version("0.66.0", sha256="c3063a85c8f17df6ba1722f06eaab74fe14a53f37f5a86664c23a7f35d943f3a")
    version("0.65.0", sha256="beb4f7bc73b746fe68c4333fa4d4e1dba05f5f5fb386874b83cbf7f105e83c45")
    version("0.64.0", sha256="1af87b410eabee7f377b047049eae486cf3161fa67546789440f1d1e56e2324d")
    version("0.63.0", sha256="32d716f52073d7ea246d01fefb420bfe5b834ebc10579edd79ebce7a87dd1a81")
    version("0.62.0", sha256="248eedc764312da401aa29304275e009196ebdb5b08594a1522bb165c16874aa")
    version("0.61.0", sha256="7b4304b7556d8ec0742d1b8a9280f7f788307d2a6f4d2f59cc8e8358b6c69c11")
    version("0.60.0", sha256="a57fce96d50a603075a8a4a583431a1a03170df4d2894ff30f84d8c5ab4caf47")
    version("0.59.0", sha256="eae5933a7b37834cf4f70424b083f99799f9381ee8bb616f3a01d4ab2e5631a6")
    version("0.58.0", sha256="6b092dda66e7cc1bc4842fe54ab41248c4f136307cc955081e8052222c82aff1")
    version("0.57.0", sha256="4f978616c13f311170fdc992610ad1fd727884cf0d20b6849b2c985d936c482b")
    version("0.56.2", sha256="1ae20415ba50a4dcfec7992e9a571f09f075f077ebdd7c1afb9a19b158f6205d")
    version("0.56.1", sha256="01b7c09f1eafff819de0079baf033f75547432be62dc10cb96691d078994a4e9")
    version("0.56.0", sha256="77003c9dde0590ca37fddfbe380b29b9f897fa0dadb9b9f953819f5e9d9f08f0")
    version("0.55.3", sha256="f8c6ae6ae48c4d38a82691d7de219ebf0e3f9ca38ae6ba31a64181bfd8a8c50a")
    version("0.55.2", sha256="47f25f27f4bff22fd32825d5a1135522e61f9505758dde3d093cfbdaff0b3255")
    version("0.55.1", sha256="39f1799d965cd0fec06f0a43dec865c360cbb206e4254f4deb4f7b7f7f3c3b2f")
    version("0.55.0", sha256="fb74cfe2a8f3da51f9840082fa563c2a4ce689972c164e95b1b8a1817c4224cf")
    version("0.54.0", sha256="cd28ddf054446c286f9bfae563aa463e638ee03e0353c0828a9ce44be4ce2df9")
    version("0.53.2", sha256="4a7b57f1fd8e3e85ecf4a481cc907b81a71c4f44cf2c4a506cb37a6513a819a4")
    version("0.53.1", sha256="1425dec7ee1a7ddf1c3086b83834ef6e49de021901a62d5bff0f2ca0c75d3455")
    version("0.53.0", sha256="0afb44c2dab8dd8121d174193eb6623b29da9592e5fe1bbe344cfc9cacbec0cb")
    version("0.52.2", sha256="c642463da0bbdd533399e43c84ea0007b1d7da98276c26bc075c7b4778f97a01")
    version("0.52.1", sha256="32f211aaf4641223bf837dc71ea064931f85aa9260b9c7f379787ca907c78c3a")
    version("0.52.0", sha256="2fd4cf0cc43c363b2e51cb264a919a1b43514aad979b9b5761b746fc70490130")
    version("0.51.0", sha256="878d5399c4789034b7f587a478e2baf8e852f7f1f82aa59e276ddf81d325b934")
    version("0.50.4", sha256="f4ab7dada0e07ecf97f88e2dd7ca6c4755fb0f4175d8d12ed3a856c45b240bde")
    version("0.50.3", sha256="cc78bfc9a5d1b061098c892e9c8ff14861aa48ea95f0e9684ca4250d30c38889")
    version("0.50.2", sha256="0ef1355f905d48ed01c034a8d418e9c528113d65acb3dd31951297029c5aaed4")
    version("0.50.1", sha256="1500bae01ba74c330bc205b57423688c2b1aacafe1aabcaf469b221dcda9beec")
    version("0.50.0", sha256="c50fb77b5c8d535fe0c930e5d4400d039ad567a571ea9711b01d6d5bd2a26fb6")
    version("0.49.2", sha256="cde90e0183024dc1a78d510e2ae3effa087c86c5761f84cba0125f10abc74254")
    version("0.49.1", sha256="6d1952ada65d52d2fd5d4c60bb17e51d264c2c618f9b66dadeffa1e5f849394a")
    version("0.49.0", sha256="adfe5c64a5d170197893fe5a4c9338cde6cbdd5b54e52534886425101be4458f")
    version("0.48.0", sha256="087a7f944240caf2d121c1520a6877beea5d30cc598d09a55138014d7953348a")
    version("0.47.0", sha256="efce0f6f32e00482b80973d951a6ddc47b20c8703bd0e63ab59acc0e339d410b")
    version("0.46.3", sha256="24bc5d8532a90f07ab2a412ea28ddbfc8ff7ab27cd9b4e7bd99a92b2a0b5acfd")
    version("0.46.2", sha256="3ebbafa241e54cb328966ea99eab5d837c4a889f17c3b2048cc2961166a84cc4")
    version("0.46.1", sha256="be7468b30a367bcbefab09ed5ac07320cd323904c9129d6b874175b39ef65cd9")
    version("0.46.0", sha256="ab944358edc7e03be604749002f1f00aaf4d55d20bac2689d40bd4e66357879d")
    version("0.45.0", sha256="b3307b99f82f0300dfed7dd122447a6e74ca8ad8c012d2fc60467e6e067ac226")
    version("0.44.0", sha256="cec114325167731233be294aab329d54862457cb2e1f1a87d42d100da7c53aa5")
    version("0.42.2", sha256="a9289260eb0a4eaf4550c2d6ad1af7e95a669a747ce425ab9a572d4ab80e2c1f")
    version("0.42.1", sha256="5f79487568ec4625b0731f0c10efb565201602a733d1b6ac1436e8934cf8b8ec")
    version("0.42.0", sha256="c08e047e202271ec15eeda53670c6082815d168009f4e993debcc0d035904d6b")
    version("0.41.0", sha256="b789360d70656d99cd5e0ceebfc8828bdf129f7e2bfe6451592a735be9a0809a")
    version("0.40.1", sha256="73a65f17e727191b97dfdf770dd2c285900af05e6fee93aa9ced9eadb86f58ff")
    version("0.40.0", sha256="80e68172eeef0fbff128ede354eaac759a9408c3ef72c5eed871bb9430b960ff")
    version("0.39.0", sha256="e62fea9bcb96529507fdd83abc991036e8ed9aa858b7d36587fce3d559420036")
    version("0.38.2", sha256="5f38387d92338eac8658cd70544a5d9a609bd632090f4f69bcbc9f07ec4abd7b")
    version("0.38.1", sha256="99ff1ff61408e17f67ab427c51add074f66ab7375a506ae70dcb24c47a8ea636")
    version("0.38.0", sha256="e95aa6e4161324fa92fa236ea2bf08a7267a883ef4ca5fbb8bbf75e70db1ce4f")
    version("0.37.0", sha256="98877fa2daf91ac91c2e0e0014684131d6efc4a1f2f77917d40fdbf424d74588")
    version("0.36.0", sha256="452a3973cf359786409e064ca4b63a5f81072a9d72a52d1a4084d197f21fc26b")
    version("0.35.0", sha256="50e6de305e1ffdcf423cec424e919bb0bdebee6449d34ff26a40421f09392826")
    version("0.34.4", sha256="5a997c6f4b8c954a98046a851d0f3b31ce7c5be6e7e615068df4f1d7b86c9630")
    version("0.34.3", sha256="1f5994862c33df4588d411b49fba20a40294627d0b325bbd5234f169eb1d4842")
    version("0.34.2", sha256="3b8d3f801799023c8efe5069895723ce4e742330282774dc0873c2fa3910eeb2")
    version("0.34.1", sha256="791ff249a685fab1733d4c3c936db6a064aa912d47926ad4bd26b1829f6e2178")
    version("0.34.0", sha256="da62a15da103e763e34dae43be3436873e4fb550630dddc55232ae644accda02")
    version("0.33.0", sha256="61200855a0846ce765b686fa368496f44534e633031811803ba2cb31f94c25b1")
    version("0.32.0", sha256="187e75fc6d3f84003829d2b8aec584e99d72d65f2d82835998714ae05ae008af")
    version("0.31.1", sha256="32c1fd8319fbbb844a0a252d44761f81f17c6f3549daadce47e81524d84605a4")
    version("0.31.0", sha256="9d4bc8b2c1a210a58f34216cebe7cd5935039d244b7e90f7e2792bda81ff7ddc")
    version("0.30.1", sha256="e2249bdced68d80a413de59f8393922553a8900a14e731030e362266e82a9af8")
    version("0.30.0", sha256="91de53099d9381e3744e7a1ac06d2db0f9065378c4d178328b78ac797ee3ec65")
    version("0.29.1", sha256="ced1e98fbd383669e59ec06d2e0c15e27dbceda9ac5569d311c538b2fe6d3876")
    version("0.29.0", sha256="a417a1d0ed75bd51131b86fba990502666d8c1388ad6282b3097aa461ccf9785")
    version("0.28.0", sha256="5c4e0fe8c7c80615688f271b57b35ee9d924ac07c6d3d56d0303e610338ed332")
    version("0.27.1", sha256="3f7d2401ff8b113781d93c5bf374f47ca35b2f962634c6310b73620da735e63d")
    version("0.27.0", sha256="387ee5958de2d986095cda2aaf39d0bf319d02eaeeea2a565aea97e6a6f31f36")
    version("0.26.0", sha256="c451591d106d1671c9ddbb5c304979dd2d083e0616b2aeede62e7a6b568f828c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "pybind", default=False, description="build support for pybind metrics", when="@0.96.0:"
    )
    variant(
        "openssl", default=False, description="build support for hashing options", when="@0.96.2:"
    )
    variant("szx", default=False, description="build support for SZx", when="@0.87.0:")
    variant("blosc2", default=False, description="build support for blosc2", when="@0.98.0:")
    variant("matio", default=False, description="build support for matio", when="@0.99.0:")
    variant("clang", default=False, description="build migration tools", when="@0.99.0:")
    variant("blosc", default=False, description="support the blosc lossless compressors")
    variant("fpzip", default=False, description="support for the FPZIP lossy compressor")
    variant("hdf5", default=False, description="support reading and writing from hdf5 files")
    variant("magick", default=False, description="support the imagemagick image compressors")
    variant(
        "mgard", default=False, description="support for the MAGARD error bounded lossy compressor"
    )
    variant("python", default=False, description="build the python wrappers")
    variant("sz", default=False, description="support for the SZ error bounded lossy compressor")
    variant("zfp", default=False, description="support for the ZFP error bounded lossy compressor")
    variant("boost", default=False, description="support older compilers using boost")
    variant("petsc", default=False, description="support IO using petsc format")
    variant("mpi", default=False, description="support for launching processes using mpi")
    variant("lua", default=False, description="support for composite metrics using lua")
    variant(
        "libdistributed", default=False, description="support for distributed multi-buffer support"
    )
    variant("ftk", default=False, description="build support for the feature tracking toolkit")
    variant("digitrounding", default=False, description="build support for the digit rounding")
    variant("bitgrooming", default=False, description="build support for the bitgrooming")
    variant("openmp", default=False, description="build plugins that use openmp")
    variant("docs", default=False, description="build and install manual pages")
    variant("remote", default=False, description="build the remote launch plugin")
    variant("json", default=False, description="build the JSON support")
    variant("szauto", default=False, description="build szauto support")
    variant("unix", default=False, description="build support for unixisms like mmap and rusage")
    variant("ndzip", default=False, description="build support for the NDZIP compressor")
    variant("arc", default=False, description="build support for the ARC error correction tool")
    variant("netcdf", default=False, description="build support for the NDFCDF data format")
    variant("sz3", default=False, description="build support for the SZ3 compressor family")
    variant("mgardx", default=False, description="build support for the MGARDx compressor")
    variant("bzip2", default=False, description="build support for the bzip2 compressor")
    variant("qoz", default=False, description="build support for the qoz compressor")
    variant("core", default=True, description="build core builtin libraries")
    variant(
        "cusz", default=False, description="build support for the cusz compressor", when="@0.86.0:"
    )

    # cufile was only added to the .run file installer for cuda in 11.7.1
    # dispite being in the APT/RPM packages for much longer
    # a external install the cufile libraries could use an earlier version
    # which provides these libraries
    depends_on("cuda@11.7.1:", when="+cuda")

    depends_on("boost", when="@:0.51.0+boost")

    depends_on("libstdcompat+boost", when="+boost")
    depends_on("libstdcompat@0.0.16:", when="@0.93.0:")
    depends_on("libstdcompat@0.0.14:", when="@0.79.0:")
    depends_on("libstdcompat@0.0.13:", when="@0.73.0:")
    depends_on("libstdcompat@0.0.10:", when="@0.71.3:")
    depends_on("libstdcompat@0.0.7:", when="@0.70.3:")
    depends_on("libstdcompat@0.0.6:", when="@0.70.2:")
    depends_on("libstdcompat@0.0.5:", when="@0.63.0:")
    depends_on("libstdcompat@0.0.3:", when="@0.60.0:")
    depends_on("libstdcompat", when="@0.52.0:")

    depends_on("c-blosc", when="+blosc")
    depends_on("fpzip", when="+fpzip")
    depends_on("hdf5", when="+hdf5")
    # this might seem excessive, but if HDF5 is external and parallel
    # we might not get the MPI compiler flags we need, so depend on this
    # explicitly
    depends_on("mpi@2:", when="+hdf5 ^hdf5+mpi")
    depends_on("imagemagick", when="+magick")
    depends_on("mgard", when="+mgard")
    depends_on("python@3:", when="+python", type=("build", "link", "run"))
    depends_on("py-numpy", when="+python", type=("build", "link", "run"))
    depends_on("swig@3.12:", when="+python", type="build")
    depends_on("sz@2.1.8.1:", when="@0.55.2:+sz")
    depends_on("sz@2.1.11.1:", when="@0.55.3:+sz")
    depends_on("sz@2.1.12:", when="@0.69.0:+sz")
    depends_on("fftw", when="+sz ^sz@:2.1.10")
    depends_on("zfp", when="+zfp")
    depends_on("petsc", when="+petsc")
    depends_on("mpi@2:", when="+mpi")
    depends_on("lua-sol2", when="+lua")
    depends_on("libdistributed@0.0.11:", when="+libdistributed")
    depends_on("libdistributed@0.4.0:", when="@0.85.0:+libdistributed")
    depends_on("pkgconfig", type="build")
    depends_on("ftk@master", when="+ftk")
    depends_on("digitrounding", when="+digitrounding")
    depends_on("bitgroomingz", when="+bitgrooming")
    depends_on("cmake@3.14:", type="build")
    depends_on("py-mpi4py", when="@0.54.0:+mpi+python", type=("build", "link", "run"))
    depends_on("py-numcodecs", when="@0.54.0:+python", type="run")
    depends_on("doxygen+graphviz", when="+docs", type="build")
    depends_on("curl", when="+remote")
    depends_on("nlohmann-json+multiple_headers", when="+remote")
    depends_on("nlohmann-json+multiple_headers", when="+json")
    depends_on("szauto", when="+szauto")
    depends_on("ndzip", when="+ndzip")
    depends_on("arc", when="+arc")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("mgardx", when="+mgardx")
    depends_on("szx@:1.1.0", when="@0.87.0:0.97.1 +szx")
    depends_on("szx@1.1.1:", when="@0.97.2: +szx")
    depends_on("openssl", when="+openssl")
    depends_on("py-pybind11", when="+pybind")
    depends_on("matio+shared@1.5.17:", when="+matio")
    depends_on("llvm@17: +clang", when="+clang")
    conflicts(
        "^ mgard@2022-11-18",
        when="@:0.88.3+mgard",
        msg="mgard@2022-11-18 is not supported before 0.89.0",
    )
    conflicts(
        "+mgardx", when="+szauto", msg="SZ auto and MGARDx cause symbol conflicts with each other"
    )
    conflicts(
        "~json",
        when="@0.57.0:+remote",
        msg="JSON support required for remote after version 0.57.0",
    )
    for cuda_compressor in ["cusz", "mgard", "zfp", "ndzip"]:
        conflicts(
            f"~cuda+{cuda_compressor} ^ {cuda_compressor}+cuda",
            msg="compiling a CUDA compressor without a CUDA support makes no sense",
        )
    depends_on("sz3", when="+sz3")
    depends_on("sz3@3.1.8:", when="@0.98.1: +sz3")
    depends_on("bzip2", when="+bzip2")
    depends_on("qoz", when="+qoz")
    depends_on("cusz@0.6.0:", when="+cusz")

    extends("python", when="+python")

    def lp_cxx_version(self):
        try:
            self.compiler.cxx20_flag
            return "20"
        except Exception:
            pass
        try:
            self.compiler.cxx17_flag
            return "17"
        except Exception:
            pass
        try:
            self.compiler.cxx14_flag
            return "14"
        except Exception:
            pass
        self.compiler.cxx11_flag
        return "11"

    def cmake_args(self):
        args = [
            self.define_from_variant("LIBPRESSIO_HAS_SZ", "sz"),
            self.define_from_variant("LIBPRESSIO_HAS_SZx", "szx"),
            self.define_from_variant("LIBPRESSIO_HAS_OPENSSL", "openssl"),
            self.define_from_variant("LIBPRESSIO_HAS_PYTHON_LAUNCH", "pybind"),
            self.define_from_variant("LIBPRESSIO_HAS_BLOSC2", "blosc2"),
            self.define_from_variant("LIBPRESSIO_HAS_MATLABIO", "matio"),
            self.define_from_variant("BUILD_MIGRATION_TOOLS", "clang"),
            self.define_from_variant("LIBPRESSIO_HAS_SZ_AUTO", "szauto"),
            self.define_from_variant("LIBPRESSIO_HAS_ZFP", "zfp"),
            self.define_from_variant("LIBPRESSIO_HAS_FPZIP", "fpzip"),
            self.define_from_variant("LIBPRESSIO_HAS_BLOSC", "blosc"),
            self.define_from_variant("LIBPRESSIO_HAS_MAGICK", "magick"),
            self.define_from_variant("LIBPRESSIO_HAS_MGARD", "mgard"),
            self.define_from_variant("LIBPRESSIO_HAS_PETSC", "petsc"),
            self.define_from_variant("LIBPRESSIO_HAS_MPI", "mpi"),
            self.define_from_variant("LIBPRESSIO_HAS_LUA", "lua"),
            self.define_from_variant("LIBPRESSIO_HAS_LIBDISTRIBUTED", "libdistributed"),
            self.define_from_variant("LIBPRESSIO_HAS_FTK", "ftk"),
            self.define_from_variant("LIBPRESSIO_HAS_BIT_GROOMING", "bitgrooming"),
            self.define_from_variant("LIBPRESSIO_HAS_DIGIT_ROUNDING", "digitrounding"),
            self.define_from_variant("LIBPRESSIO_HAS_OPENMP", "openmp"),
            self.define_from_variant("LIBPRESSIO_HAS_REMOTELAUNCH", "remote"),
            self.define_from_variant("LIBPRESSIO_HAS_JSON", "json"),
            self.define_from_variant("LIBPRESSIO_HAS_LINUX", "unix"),
            self.define_from_variant("LIBPRESSIO_HAS_NDZIP", "ndzip"),
            self.define_from_variant("LIBPRESSIO_HAS_ARC", "arc"),
            self.define_from_variant("LIBPRESSIO_HAS_NETCDF", "netcdf"),
            self.define_from_variant("LIBPRESSIO_HAS_SZ3", "sz3"),
            self.define_from_variant("LIBPRESSIO_HAS_MGARDx", "mgardx"),
            self.define_from_variant("LIBPRESSIO_HAS_BZIP2", "bzip2"),
            self.define_from_variant("LIBPRESSIO_HAS_QoZ", "qoz"),
            self.define_from_variant("LIBPRESSIO_HAS_CUSZ", "cusz"),
            self.define_from_variant("LIBPRESSIO_HAS_CUFILE", "cuda"),
            self.define_from_variant("LIBPRESSIO_HAS_CUDA", "cuda"),
            self.define_from_variant("LIBPRESSIO_HAS_HDF", "hdf5"),
            self.define_from_variant("BUILD_DOCS", "docs"),
            self.define_from_variant("LIBPRESSIO_INSTALL_DOCS", "docs"),
            self.define_from_variant("BUILD_PYTHON_WRAPPER", "python"),
            self.define("LIBPRESSIO_HAS_MPI4PY", self.spec.satisfies("+python +mpi")),
            self.define(
                "LIBPRESSIO_BUILD_MODE", "FULL" if self.spec.satisfies("+core") else "CORE"
            ),
            self.define("BUILD_TESTING", self.run_tests),
            # this flag was removed in 0.52.0, we should deprecate and remove this
            self.define(
                "LIBPRESSIO_CXX_VERSION",
                "11" if self.spec.satisfies("+boost") else self.lp_cxx_version(),
            ),
        ]
        # if cuda is backed by the shim, we need to set these linker flags to
        # avoid downstream linker errors
        if self.spec.satisfies("+cusz +cuda"):
            args.append("-DCMAKE_EXE_LINKER_FLAGS=-Wl,--allow-shlib-undefined")
        # libpressio needs to know where to install the python libraries
        if self.spec.satisfies("+python"):
            args.append(f"-DLIBPRESSIO_PYTHON_SITELIB={python_platlib}")
        # help ensure that libpressio finds the correct HDF5 package
        if self.spec.satisfies("+hdf5"):
            args.append("-DHDF5_ROOT=" + self.spec["hdf5"].prefix)
        return args

    def setup_run_environment(self, env):
        if self.spec.satisfies("+hdf5") and self.spec.satisfies("+json"):
            env.prepend_path("HDF5_PLUGIN_PATH", self.prefix.lib64)

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        make("test")

    @run_after("build")
    def install_docs(self):
        if self.spec.satisfies("+docs"):
            with working_dir(self.build_directory):
                make("docs")

    @run_after("install")
    def copy_test_sources(self):
        if self.spec.satisfies("@:0.88.2"):
            return
        srcs = [
            join_path("test", "smoke_test", "smoke_test.cc"),
            join_path("test", "smoke_test", "CMakeLists.txt"),
        ]
        cache_extra_test_sources(self, srcs)

    def test_smoke(self):
        """Run smoke test"""
        # this works for cmake@3.14: which is required for this package
        if self.spec.satisfies("@:0.88.2"):
            raise SkipTest("Package must be installed as version @0.88.3 or later")

        args = self.cmake_args()
        args.append(f"-S{join_path(self.test_suite.current_test_cache_dir, 'test', 'smoke_test')}")
        args.append(f"-DCMAKE_PREFIX_PATH={self.spec['libstdcompat'].prefix};{self.prefix}")

        cmake = self.spec["cmake"].command
        cmake(*args)
        cmake("--build", ".")

        exe = which("pressio_smoke_tests")
        out = exe(output=str.split, error=str.split)

        expected = "all passed"
        assert expected in out
