import pytest
import brownie
import time

TARGET_2 = 100
ENDTIME_2 = int(time.time() + 20)


@pytest.fixture(scope="function", autouse=True)
def crowd_contract(Crowdfunding, accounts):

    # deploy the contract with the initial values as a constructor argument
    yield Crowdfunding.deploy(TARGET_2, ENDTIME_2, {'from': accounts[0]})


def test_initial_state(crowd_contract):
    # Check if the constructor of the contract is set up properly
    assert crowd_contract.target() == TARGET_2
    assert crowd_contract.deadline() == ENDTIME_2


def test_fund(crowd_contract, accounts):

    # Funding Test
    crowd_contract.donate({'from': accounts[2], 'value': 10})
    assert crowd_contract.donations(
        accounts[2].address) == 10  # Directly access donations

    # Funding Test Other account
    crowd_contract.donate({'from': accounts[1], 'value': 20})
    assert crowd_contract.donations(
        accounts[1].address) == 20  # Directly access donations

    # Funding Finish Before end
    with brownie.reverts():
        crowd_contract.finish({"from": accounts[0]})

    time.sleep(20)

    # Donate after end
    with brownie.reverts():
        crowd_contract.donate({"from": accounts[3], 'value': 10})

    # Non owner finish
    with brownie.reverts():
        crowd_contract.finish({"from": accounts[1]})

    # Finish not target
    with brownie.reverts():
        crowd_contract.finish({"from": accounts[0]})

    # Refund
    crowd_contract.withdraw({'from': accounts[2]})
    assert crowd_contract.donations(
        accounts[2].address) == 0  # Directly access donations

    # Refund Non donator
    with brownie.reverts():
        crowd_contract.withdraw({'from': accounts[3]})
