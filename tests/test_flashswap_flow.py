#!/usr/bin/python3
from brownie import interface, Opportunity, FlashSwapPancake
import brownie
import eth_abi

# Test whether deployed contracts withdrawal function can only be called by owner
def test_contracts_withdrawal_only_owner(accounts,deploy_fund_flashswap_and_opportunity,fund_owner_from_whale):
    deploy_flashswap, deploy_opportunity = deploy_fund_flashswap_and_opportunity
    token_contract = fund_owner_from_whale

    # call withdrawAllBalance on both contracts with non-owner account
    with brownie.reverts("Ownable: caller is not the owner"):
        flashswap_withdraw_txn = deploy_flashswap.withdrawAllBalance(token_contract.address,{"from": accounts[1]})
        flashswap_withdraw_txn.wait(1)
    with brownie.reverts("Ownable: caller is not the owner"):
        opportunity_withdraw_txn = deploy_opportunity.withdrawAllBalance(token_contract.address,{"from": accounts[1]})
        opportunity_withdraw_txn.wait(1)

    # call withdrawAllBalance on both contracts with owner account
    flashswap_withdraw_txn = deploy_flashswap.withdrawAllBalance(token_contract.address,{"from": accounts[0]})
    flashswap_withdraw_txn.wait(1)

    opportunity_withdraw_txn = deploy_opportunity.withdrawAllBalance(token_contract.address,{"from": accounts[0]})
    opportunity_withdraw_txn.wait(1)

    assert flashswap_withdraw_txn.status == 1
    assert opportunity_withdraw_txn.status == 1
    
# Test whether deployed contracts can successfully withdraw all balance
def test_contracts_withdrawal(accounts,deploy_fund_flashswap_and_opportunity,fund_owner_from_whale):
    deploy_flashswap, deploy_opportunity = deploy_fund_flashswap_and_opportunity
    token_contract = fund_owner_from_whale

    # call withdrawAllBalance on both contracts
    flashswap_withdraw_txn = deploy_flashswap.withdrawAllBalance(token_contract.address,{"from": accounts[0]})
    flashswap_withdraw_txn.wait(1)
    opportunity_withdraw_txn = deploy_opportunity.withdrawAllBalance(token_contract.address,{"from": accounts[0]})
    opportunity_withdraw_txn.wait(1)

    assert flashswap_withdraw_txn.status == 1
    assert opportunity_withdraw_txn.status == 1

# Test whether the flashswap function can be successfully executed
def test_flashswap(accounts,deploy_fund_flashswap_and_opportunity,fund_owner_from_whale):
    deploy_flashswap, deploy_opportunity = deploy_fund_flashswap_and_opportunity
    token_contract = fund_owner_from_whale
    pool_contract_address = "0x7EFaEf62fDdCCa950418312c6C91Aef321375A00"

    # call flashswap on flashswap contract
    secret_key = "lets_really_hope_i_dont_burn_more_money"
    encoded_data = eth_abi.encode_single(
        '(bool,uint256,address,address,string)',  
        (
            False,
            1 * 10 ** 18,
            token_contract.address,
            deploy_opportunity.address,
            secret_key
        )
    ).hex()
    execute_flashloan = deploy_flashswap.borrowFlashloan(pool_contract_address, token_contract.address, False, 1 * 10 ** 18,encoded_data, {"from": accounts[0]})
    execute_flashloan.wait(1)

    assert execute_flashloan.status == 1

# Test whether the opportunity contract's function payAndSolveHash can be successfully executed
def test_opportunity(accounts,deploy_fund_flashswap_and_opportunity,fund_owner_from_whale):
    deploy_flashswap, deploy_opportunity = deploy_fund_flashswap_and_opportunity
    token_contract = fund_owner_from_whale

    # call payAndSolveHash on opportunity contract
    approve_spender = token_contract.approve(deploy_opportunity, 1 * 10 ** 18, {"from": accounts[0]})
    approve_spender.wait(1)

    solve_hash_and_pay = deploy_opportunity.solveHashAndPay("lets_really_hope_i_dont_burn_more_money",{"from": accounts[0]})
    solve_hash_and_pay.wait(1)

    assert solve_hash_and_pay.status == 1

