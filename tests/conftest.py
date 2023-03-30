#!/usr/bin/python3

import pytest
from brownie import interface

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def fund_owner_from_whale(accounts):
    whale_address = "0xf977814e90da44bfa03b6295a0616a897441acec"
    whale = accounts.at(whale_address, force=True)

    token_address =  "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
    token = interface.IERC20(token_address)

    # fund owner with 100 units of token
    fund_owner = token.transfer(accounts[0], 100 * 10 ** 18, {"from":whale})
    fund_owner.wait(1)

    return token

@pytest.fixture(scope="module")
def deploy_fund_flashswap_and_opportunity(accounts,FlashSwapPancake,Opportunity,fund_owner_from_whale):
    token = fund_owner_from_whale

    # deploy both contracts
    deploy_flashswap = FlashSwapPancake.deploy({'from': accounts[0]})
    dummy_hash = "0xc27e502ac6adf5b5187091940e1557442732d446b1022acb3f723f321c6e2de1"
    deploy_opportunity = Opportunity.deploy(token.address, dummy_hash, 18,{'from': accounts[0]})    

    # fund flashswap contract with 1 unit of token
    fund_flashswap = token.transfer(deploy_flashswap, 1 * 10 ** 18, {"from":accounts[0]})
    fund_flashswap.wait(1)

    # fund opportunity contract with 5 units of token
    fund_opportunity = token.transfer(deploy_opportunity, 5 * 10 ** 18, {"from":accounts[0]})
    fund_opportunity.wait(1)

    return deploy_flashswap, deploy_opportunity
