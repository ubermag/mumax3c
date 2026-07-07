import pytest

import mumax3c as mc

not_supported_by_mumax = [
    "test_demag_demag_asymptotic_radius",
    "test_energy_zeeman_zeeman",
    "test_exchange_field",
    "test_simple_hysteresis_loop",
    "test_stepped_hysteresis_loop",
    "test_hysteresis_check_for_energy",
    "test_min_driver_evolver_nodriver",
    "test_min_driver_evolver_driver",
    "test_min_driver_wrong_evolver",
    "test_outputstep",
    "test_precession_field",
    "test_rkky_scalar",
    "test_threads_threads",
    "test_time_driver_rungekutta_evolver_nodriver",
    "test_time_driver_euler_evolver_nodriver",
    "test_time_driver_theta_evolver_nodriver",
    "test_time_driver_therm_heun_evolver_nodriver",
    "test_time_driver_noevolver_nodriver_finite_temperature",
    "test_time_driver_wrong_evolver",
    "test_time_driver_noevolver_driver",
    "test_zeeman_time_vector",
    "test_zeeman_time_dict",
    "test_zeeman_time_field",
    "test_min_driver_noevolver_driver",
    "test_dmi_crystalclass",
    "test_cubic_anisotropy_field_field_field",
    "test_damping_field",
    "test_dynamics_field_field",
    "test_slonczewski_field_values",
    "test_zhang_li_time_tcl_scalar_u",
    "test_uniaxial_anisotropy_field_vector",
    "test_uniaxial_anisotropy_scalar_field",
    "test_uniaxial_anisotropy_field_field",
    "test_uniaxial_anisotropy_field_dict",
]

missing_in_mumax3c = [
    "test_compute_energy",
    "test_compute_energy_density",
    "test_compute_effective_field",
    "test_compute_invalid_func",
    "test_compute_dmi",
    "test_compute_slonczewski",
    "test_compute_zhang_li",
    "test_cubic_anisotropy_field_vector_vector",
    "test_damping_dict",
    "test_dynamics_scalar_dict",
    "test_fixed_subregions_fixed_subregions",
    "test_slonczewski_single_values",
    "test_slonczewski_single_values_finite_temperature",
    "test_slonczewski_dict_values",
    "test_zhang_li_time_func_scalar_u",
    "test_multiple_drives_compute",
    "test_precession_scalar",
    "test_dmi_scalar",
    "test_dmi_dict",
    "test_damping_scalar",
    "test_precession_dict",
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
