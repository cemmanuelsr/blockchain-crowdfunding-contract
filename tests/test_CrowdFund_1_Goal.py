import pytest
import brownie
import time

TARGET_1 = 30
ENDTIME_1 = int(time.time() + 10)


@pytest.fixture(scope="function", autouse=True)
def crowd_contract_ok(Crowdfunding, accounts):

    # deploy the contract with the initial values as a constructor argument
    yield Crowdfunding.deploy(TARGET_1, ENDTIME_1, {'from': accounts[0]})


def test_initial_state(crowd_contract_ok):
    # Check if the constructor of the contract is set up properly
    assert crowd_contract_ok.target() == TARGET_1
    assert crowd_contract_ok.deadline() == ENDTIME_1


def test_fund(crowd_contract_ok, accounts):

    # Funding Test
    crowd_contract_ok.donate({'from': accounts[2], 'value': 10})
    assert crowd_contract_ok.donations(
        accounts[2].address) == 10  # Directly access donations

    # Funding Test Other account
    crowd_contract_ok.donate({'from': accounts[1], 'value': 20})
    assert crowd_contract_ok.donations(
        accounts[1].address) == 20  # Directly access donations

    # Funding Finish Before end
    with brownie.reverts():
        crowd_contract_ok.finish({"from": accounts[0]})

    time.sleep(10)

    # Donate after end
    with brownie.reverts():
        crowd_contract_ok.donate({"from": accounts[3], 'value': 10})

    # Revert when target
    with brownie.reverts():
        crowd_contract_ok.withdraw({'from': accounts[2]})

    # Revert when target
    with brownie.reverts():
        crowd_contract_ok.withdraw({'from': accounts[1]})

    # Non owner finish
    with brownie.reverts():
        crowd_contract_ok.finish({'from': accounts[1]})

    # Finish
    crowd_contract_ok.finish({"from": accounts[0]})
