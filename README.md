# Blockchain Flashloan Lets get Front-runned!

I've written an article that walks through more about this code and project.
Essentially, this code is for GETTING FRONT-RUNNED. It's a fun example that I wanted to showcase so everyone can better understand and learn what front-running is like! This Repo if you use it on the BSC mainnet, WILL MOST LIKELY GET FRONT-RUNNED!

The aim is to walk through how front-running can occur on the Blockchain network. The code is not meant for production and is unoptimized.

It uses 2 main smart contracts :

- A flashswap contract [`contracts/FlashSwap.sol::brownie-frontrun-arb`](contracts/FlashSwap.sol) : This contract is able to borrow flashloans and execute functions to perform some operations and then return back the borrowed loans with interest. It uses the Pancakeswap's IUniswapV2Pair and calls it with a non-zero data parameter, which then triggers a flashloan in a callback function defined as pancakecall.

- A opportunity contract [`contracts/Opportunity.sol::brownie-frontrun-arb`](contracts/Opportunity.sol) : This contract simply pays out its entire balance to any user who knows the input of some KECCAK256 hash and who transfers 0.1 Unit of some set ERC20 token. It is initially funded with 5 BUSD of the unlocked accounts money, or by an impersonated whale if you run it on the forked network.

## Deployment

To deploy the logic of this entire system, you can deploy the transactions on the testnet or mainnet for Binance Smart Chain. For mainnet, do change the private_key and is_true variable inside the deploy_contracts.py script. To run it locally would require a deployment of BUSD ERC20 token along with a liquidity pool, so to save headache just rely on using the bsc networks.

Before running the scripts you need to download the following dependencies:

```bash
pip3 install brownie
brownie pm install Uniswap/v2-core@1.0.0
brownie pm install OpenZeppelin/openzeppelin-contracts@4.8.2
```

To run the scripts simply type :

```bash
brownie run scripts/deploy_contracts --network bsc-main-fork
```

This returns

```bash
Brownie v1.17.2 - Python development framework for Ethereum

TokenProject is the active project.

Launching 'ganache-cli --accounts 10 --hardfork istanbul --fork https://bsc-dataseed.binance.org --gasLimit 12000000 --mnemonic brownie --port 8545 --chainId 56'...

Running 'scripts/deploy_contracts.py::main'...
Transaction sent: 0x91238cbad645f1b61e7bf49dc9e035b71548e5515fa0caa277ab8c3e4148dfd6
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3846
  FlashSwapPancake.constructor confirmed   Block: 26859911   Gas used: 688365 (5.74%)
  FlashSwapPancake deployed at: 0x4A801468300b497AB11e368C90a505e93D574aF0

Transaction sent: 0x998a2cd6700228b86e096716cae2ecc6891472d8e58f8fb18ccfd68007d9c17c
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3847
  Opportunity.constructor confirmed   Block: 26859912   Gas used: 585241 (4.88%)
  Opportunity deployed at: 0x012c5C564c3E061ec5bB36E99D56EE364bAb7C49

Transaction sent: 0x0716c5490142205ff104511ff4d9e75069a7684ef5dbd2e69986ce248f426e19
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3848
  FlashSwapPancake.withdrawAllBalance confirmed   Block: 26859913   Gas used: 31948 (0.27%)

  FlashSwapPancake.withdrawAllBalance confirmed   Block: 26859913   Gas used: 31948 (0.27%)

Transaction sent: 0x8e0cc635d7349ee7e98fc8cbd3b5bc21ce2dd5f1e6f945ed93506f7c804626fb
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3849
  Opportunity.withdrawAllBalance confirmed   Block: 26859914   Gas used: 31957 (0.27%)

  Opportunity.withdrawAllBalance confirmed   Block: 26859914   Gas used: 31957 (0.27%)

Transaction sent: 0xf10eae1b8b1d7c670b5c8beb264abd4b78b0c7aefaf57c42e9893ae85fbdb119
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3850
  IERC20.transfer confirmed   Block: 26859915   Gas used: 36103 (0.30%)

  IERC20.transfer confirmed   Block: 26859915   Gas used: 36103 (0.30%)

Transaction sent: 0x34e40a68ce32c5b9266de4d4617e04d8e7dd223c3bfa776e66444d3bc5e67e4d
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3851
  IERC20.transfer confirmed   Block: 26859916   Gas used: 36103 (0.30%)

  IERC20.transfer confirmed   Block: 26859916   Gas used: 36103 (0.30%)

Initial Fund FlashSwap balance:  1000000000000000000
Transaction sent: 0x2e7859cb3de747d9b3154596ed65f8c51d302443420a320928a684d34172bea1
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3852
  FlashSwapPancake.borrowFlashloan confirmed   Block: 26859917   Gas used: 150239 (1.25%)

  FlashSwapPancake.borrowFlashloan confirmed   Block: 26859917   Gas used: 150239 (1.25%)

Final FlashSwap balance:  5996990972918756268
Final Opportunity balance:  0
Final profit:  4996990972918756268
```

## Testing

To run the tests and check the gas of each tranasction for interesting and a prettified response:

```bash
brownie test  --network bsc-main-fork --gas
```

```bash
Launching 'ganache-cli --accounts 10 --hardfork istanbul --fork https://bsc-dataseed.binance.org --gasLimit 12000000 --mnemonic brownie --port 8545 --chainId 56'...

tests/test_flashswap_flow.py ....                                                                                                      [100%]
================================================================ Gas Profile =================================================================


FlashSwapPancake <Contract>
   ├─ constructor        -  avg: 688365  avg (confirmed): 688365  low: 688365  high: 688365
   ├─ borrowFlashloan    -  avg: 150239  avg (confirmed): 150239  low: 150239  high: 150239
   └─ withdrawAllBalance -  avg:  24816  avg (confirmed):  25348  low:  22693  high:  25348
Opportunity <Contract>
   ├─ constructor        -  avg: 585241  avg (confirmed): 585241  low: 585241  high: 585241
   ├─ solveHashAndPay    -  avg:  43800  avg (confirmed):  43800  low:  43800  high:  43800
   └─ withdrawAllBalance -  avg:  24831  avg (confirmed):  25357  low:  22731  high:  25357
Token <Contract>
   ├─ transfer           -  avg:  51103  avg (confirmed):  51103  low:  51091  high:  51115
   └─ approve            -  avg:  44094  avg (confirmed):  44094  low:  44094  high:  44094

============================================================= 4 passed in 14.10s =============================================================
```

The unit tests included are quite basic and the relevant fixtures for the test are defined in [`tests/conftest.py::brownie-frontrun-arb`](tests/conftest.py) fixture.
