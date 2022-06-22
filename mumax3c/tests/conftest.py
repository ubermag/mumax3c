import pytest

import mumax3c as mc

not_supported_by_mumax = [
    "TestDemag.test_demag_asymptotic_radius",
    "TestEnergy.test_zeeman_zeeman",
    "TestExchange.test_field",
    "TestHysteresisDriver.test_noevolver_nodriver",
    "TestMinDriver.test_evolver_nodriver",
    "TestMinDriver.test_evolver_driver",
    "TestMinDriver.test_wrong_evolver",
    "test_outputstep",
    "TestPrecession.test_field",
    "TestRKKY.test_scalar",
    "TestThreads.test_threads",
    "TestTimeDriver.test_rungekutta_evolver_nodriver",
    "TestTimeDriver.test_euler_evolver_nodriver",
    "TestTimeDriver.test_theta_evolver_nodriver",
    "TestTimeDriver.test_therm_heun_evolver_nodriver",
    "TestTimeDriver.test_noevolver_nodriver_finite_temperature",
    "TestTimeDriver.test_wrong_evolver",
    "TestTimeDriver.test_noevolver_driver",
    "TestZeeman.test_time_vector",
    "TestZeeman.test_time_dict",
    "TestZeeman.test_time_field",
    "TestMinDriver.test_noevolver_driver",
    "TestDMI.test_crystalclass",
    "TestCubicAnisotropy.test_field_field_field",
    "TestDamping.test_field",
    "TestDynamics.test_field_field",
    "TestSlonczewski.test_field_values",
    "TestZhangLi.test_field_scalar",
    "TestUniaxialAnisotropy.test_field_vector",
    "TestUniaxialAnisotropy.test_scalar_field",
    "TestUniaxialAnisotropy.test_field_field",
    "TestUniaxialAnisotropy.test_field_dict",
]

missing_in_mumax3c = [
    "TestCompute.test_energy",
    "TestCompute.test_energy_density",
    "TestCompute.test_effective_field",
    "TestCompute.test_invalid_func",
    "TestCompute.test_dmi",
    "TestCompute.test_slonczewski",
    "TestCompute.test_zhang_li",
    "TestCubicAnisotropy.test_field_vector_vector",
    "TestDamping.test_dict",
    "TestDynamics.test_scalar_dict",
    "TestFixedSubregions.test_fixed_subregions",
    "TestSlonczewski.test_single_values",
    "TestSlonczewski.test_single_values_finite_temperature",
    "TestSlonczewski.test_dict_values",
    "TestZhangLi.test_dict_scalar",
    "TestZhangLi.test_time_scalar_scalar",
    "test_multiple_drives_compute",
    "TestZhangLi.test_scalar_scalar",
    "TestPrecession.test_scalar",
    "TestDMI.test_scalar",
    "TestDMI.test_dict",
    "TestDamping.test_scalar",
    "TestPrecession.test_dict",
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
