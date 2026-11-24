from contracts.milestone_verifier import GrantMilestoneVerifier


def test_contract_methods_exist():
    assert hasattr(GrantMilestoneVerifier, "register_milestone")
    assert hasattr(GrantMilestoneVerifier, "verify_and_settle_milestone")
    assert hasattr(GrantMilestoneVerifier, "get_milestone")
