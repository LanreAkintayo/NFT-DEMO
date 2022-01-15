import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time

def test_can_create_advanced_collectible_integration():
    """
    Check if tokenCounter will equal 1 in rinkeby test network
    """
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for real networks")

    account = get_account()

    advancedCollectible, transaction = deploy_and_create()

    time.sleep(60)

    assert advancedCollectible.tokenCounter() == 1




    