from brownie import AdvancedCollectible, config, network
from scripts.helpful_scripts import get_contract, get_account, fund_with_link

def deploy_and_create():
    account = get_account()

    advancedCollectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source = config["networks"][network.show_active()].get("verify", False)
    )

    fund_with_link(advancedCollectible.address)

    tx = advancedCollectible.createCollectible({"from": account})
    tx.wait(1)

    print("New token has been created")

    return advancedCollectible, tx

    

def main():
    deploy_and_create()