from brownie import accounts, interface, Opportunity, FlashSwapPancake
import brownie
import eth_abi

# parameters for BSC mainnet deployment
network_name = "BSC"
busd_token_whale_address = "0xf977814e90da44bfa03b6295a0616a897441acec"
token_contract_address = "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
pool_contract_address = "0x7EFaEf62fDdCCa950418312c6C91Aef321375A00"

# shared parameters
is_test = True
private_key = "some_private_key"

#  function to control whale address balances for testing
def impersonate_whale(whale_adress):
    whale_account = accounts.at(whale_adress, force=True)
    return whale_account

# define a method to get the account, current implementation uses private key directly -> NOT RECOMMENDED
def unlock_account(address_private_key):
    accounts.add(address_private_key)
    return accounts[-1]

def main():
    # get account to deploy
    account_to_deploy = impersonate_whale(busd_token_whale_address) if is_test else unlock_account(private_key)

    # get token contract by interface at address
    token = interface.IERC20(token_contract_address)
    decimals = 18

    # deploy flashswap contract
    flashSwap = FlashSwapPancake.deploy({'from': account_to_deploy})

    # deploy opportunity contract
    secret_key = "lets_really_hope_i_dont_burn_more_money"
    secret_hash = "0xc27e502ac6adf5b5187091940e1557442732d446b1022acb3f723f321c6e2de1"
    opportunity = Opportunity.deploy(token_contract_address, secret_hash, decimals, {'from': account_to_deploy})


    # test withdrawBalance on both contracts
    flashswap_withdraw_txn = flashSwap.withdrawAllBalance(token_contract_address,{"from": account_to_deploy})
    flashswap_withdraw_txn.wait(1)
    opportunity_withdraw_txn = opportunity.withdrawAllBalance(token_contract_address,{"from": account_to_deploy})
    opportunity_withdraw_txn.wait(1)

    # send 5 BUSD to opportunity contract
    fund_opportunity = token.transfer(opportunity, 5 * 10 ** 18, {"from":account_to_deploy})
    fund_opportunity.wait(1)

    # send 1 BUSD to flashswap contract
    fund_flashswap = token.transfer(flashSwap, 1 * 10 ** 18, {"from":account_to_deploy})
    fund_flashswap.wait(1)
    initial_flashswap_balance = token.balanceOf(flashSwap)

    print("Initial Fund FlashSwap balance: ", initial_flashswap_balance)

    # execute flashloan
    encoded_data = eth_abi.encode_single(
        '(bool,uint256,address,address,string)',  
        (
            False,
            1 * 10 ** 18,
            token_contract_address,
            opportunity.address,
            secret_key
        )
    ).hex()
    execute_flashloan = flashSwap.borrowFlashloan(pool_contract_address, token_contract_address, False, 1 * 10 ** 18,encoded_data, {"from": accounts[-1]})
    execute_flashloan.wait(1)
    final_flashswap_balance = token.balanceOf(flashSwap)

    print("Final FlashSwap balance: ", final_flashswap_balance)
    print("Final Opportunity balance: ", token.balanceOf(opportunity))

    # calculate final profit for flashSwap contract
    final_profit = final_flashswap_balance - initial_flashswap_balance
    print("Final profit: ", final_profit)





