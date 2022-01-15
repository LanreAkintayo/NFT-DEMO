from brownie import network, config, accounts, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

breed_number_to_breed = {
    0: "PUG",
    1: "SHIBA_INU",
    2: "ST_BERNARD"
}

def get_breed(breed_number):
    return breed_number_to_breed[breed_number]


def get_account(index=None, id=None):
    """
    1. if index is specified, use accounts[index]
    2. if accountId is specified, use that account
    3. if we are on a development environment, use accounts[0]
    4. if we are on a test network generate your account from the private key in brownie-config.yaml,
    """

    # 1
    if index:
        return accounts[index]

    # 2
    if id:
        return accounts.load(id)

    # 3
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]

    # 4
    return accounts.add(config["wallets"]["from_key"])    

contract_to_mock = {
    "link": LinkToken,
    "vrf_coordinator": VRFCoordinatorMock

}

def get_contract(contract_name):
    """
    If we are on a local network, we deploy mock and return the latest mock deployed
    If we are on a real network, we use the abi and the address of the contract to return a mock contract
    """
    account = get_account()
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mock()
        
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    
    return contract

def deploy_mock():
    account = get_account()
    print("Deploying LinkToken Mock")

    link_token = LinkToken.deploy({"from": account})
    print("Deployed!\n")

    print("Deploying VRFCoordinatorMock Mock")
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!\n")
    


def fund_with_link(contract_address, amount=100000000000000000, account=None):
    account = account if account else get_account()

    link_token_contract = get_contract("link")
    tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)

    in_ether = Web3.fromWei(amount, "ether")
    
    print(f"{contract_address} has been funded with {in_ether} LINK")
    
