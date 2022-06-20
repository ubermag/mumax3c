import pytest

import mumax3c as mc

not_supported_by_mumax = [
    "TestExchange.test_field",
]

missing_in_mumax3c = [
    "TestRKKY.test_scalar",
]


@pytest.fixture(scope="module")
def calculator():
    return mc


@pytest.fixture(autouse=True)
def skip_unsupported_or_missing(request):
    requesting_test_function = (
        f"{request.cls.__name__}.{request.function.__name__}"
        if request.cls
        else request.function.__name__
    )
    if requesting_test_function in not_supported_by_mumax:
        pytest.skip("Not supported by mumax3.")
    elif requesting_test_function in missing_in_mumax3c:
        pytest.xfail("Currently not implemented in mumax3c.")
