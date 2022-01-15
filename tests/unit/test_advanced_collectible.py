from brownie import accounts, config, network
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import fund_with_link, get_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest

def test_can_create_advanced_collectible():
    """
    Test if tokenCounter == 1 after creating a collectible
    Test if the breed is what we expect
    """
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    advancedCollectible, transaction = deploy_and_create()

    request_id = transaction.events["requestedIdToSender"]["requestId"]
    random_number = 777

    vrf_coordinatorMock_contract = get_contract("vrf_coordinator")
    vrf_coordinatorMock_contract.callBackWithRandomness(request_id, random_number, advancedCollectible.address, {"from": account})

    assert advancedCollectible.tokenCounter() == 1
    assert advancedCollectible.tokenIdtoBreed(0) == random_number % 3

    # Because we are testing, we will need to explicitly behave like the chainlink node and call the # callBackWithRandomness() method of the VRFCoordinatorMock smart contract
