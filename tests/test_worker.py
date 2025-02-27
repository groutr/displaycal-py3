# -*- coding: utf-8 -*-

import io
import pytest

from DisplayCAL import ICCProfile
from DisplayCAL.dev.mocks import check_call_str
from DisplayCAL.worker import make_argyll_compatible_path, Worker

from tests.data.display_data import DisplayData


def test_get_options_from_profile_1(data_files):
    """Test ``DisplayCAL.worker.get_options_from_profile()`` function"""
    from DisplayCAL.worker import get_options_from_profile

    profile_path = data_files[
        "UP2516D #1 2022-03-23 16-06 D6500 2.2 F-S XYZLUT+MTX.icc"
    ].absolute()
    options = get_options_from_profile(profile=profile_path)
    assert options == (
        [
            "t6500",
            "g2.2",
            "f1.0",
            "A4.0",
            "d1",
            "c1",
            "yl",
            "P0.48923385077616427,0.8797619047619047,1.4894179894179895",
            "H",
        ],
        ["qh", "aX", 'A "Dell, Inc."'],
    )


def test_get_options_from_profile_2(data_files):
    """Test ``DisplayCAL.worker.get_options_from_profile()`` function, for #69"""
    from DisplayCAL.worker import get_options_from_profile

    profile_path = data_files["SW271 PM PenalNative_KB1_160_2022-03-17.icc"].absolute()
    options = get_options_from_profile(profile=profile_path)
    assert options == ([], [])  # no options on that profile


def test_make_argyll_compatible_path_1():
    """testing if make_argyll_compatible_path is working properly with bytes input"""
    test_value = "C:\\Program Files\\some path\\excutable.exe"
    result = make_argyll_compatible_path(test_value)
    expected_result = "C_Program Files_some path_excutable.exe"
    assert result == expected_result


def test_make_argyll_compatible_path_2():
    """testing if make_argyll_compatible_path is working properly with bytes input"""
    test_value = b"C:\\Program Files\\some path\\excutable.exe"
    result = make_argyll_compatible_path(test_value)
    expected_result = b"C_Program Files_some path_excutable.exe"
    assert result == expected_result


def test_worker_get_instrument_name_1():
    """testing if the Worker.get_instrument_name() is working properly"""
    worker = Worker()
    result = worker.get_instrument_name()
    expected_result = ""
    assert result == expected_result


def test_worker_get_instrument_features():
    """testing if Worker.get_instrument_features() is working properly"""
    worker = Worker()
    result = worker.get_instrument_features()
    assert result == {}


def test_worker_instrument_supports_css_1():
    """testing if Worker.instrument_supports_ccss is working properly"""
    worker = Worker()
    result = worker.instrument_supports_ccss()
    expected_result = None
    assert result == expected_result


def test_generate_b2a_from_inverse_table(data_files, argyll):
    """Test Worker.generate_B2A_from_inverse_table() method"""
    worker = Worker()
    icc_profile1 = ICCProfile.ICCProfile(
        profile=data_files[
            "Monitor 1 #1 2022-03-09 16-13 D6500 2.2 F-S XYZLUT+MTX.icc"
        ].absolute()
    )
    logfile = io.StringIO()
    result = worker.generate_B2A_from_inverse_table(icc_profile1, logfile=logfile)
    assert result is True


def test_get_argyll_version_1(argyll):
    """Test worker.get_argyll_version() function."""
    from DisplayCAL.worker import get_argyll_version

    with check_call_str("DisplayCAL.worker.base_get_argyll_version_string", "2.3.0"):
        result = get_argyll_version("ccxxmake")
    expected_result = [2, 3, 0]
    assert result == expected_result


def test_sudo_class_initialization():
    """Test worker.Sudo class initialization"""
    from DisplayCAL.worker import Sudo

    sudo = Sudo()
    assert sudo is not None


def test_download_method_1():
    """Test Worker.download() method."""
    from DisplayCAL.meta import DOMAIN
    from DisplayCAL.worker import Worker

    worker = Worker()
    uri = f"https://{DOMAIN}/i1d3"
    result = worker.download(uri)
    assert result is not None


def test_download_method_2():
    """Test Worker.download() method."""
    from DisplayCAL.meta import DOMAIN
    from DisplayCAL.worker import Worker

    worker = Worker()
    uri = f"https://{DOMAIN}/i1d3"
    result = worker.download(uri, force=True)
    assert result is not None


def test_download_method_3():
    """Test Worker.download() method."""
    from DisplayCAL.meta import DOMAIN
    from DisplayCAL.worker import Worker

    worker = Worker()
    uri = f"https://{DOMAIN}/spyd2"
    result = worker.download(uri)
    assert result is not None


def test_download_method_4():
    """Test Worker.download() method."""
    from DisplayCAL.meta import DOMAIN
    from DisplayCAL.worker import Worker

    worker = Worker()
    uri = f"https://{DOMAIN}/spyd2"
    result = worker.download(uri, force=True)
    assert result is not None


def test_get_display_name_1():
    """Testing Worker.get_display_name() method."""
    from DisplayCAL.worker import Worker
    from DisplayCAL.config import initcfg, setcfg

    initcfg()
    setcfg("display.number", 1)
    worker = Worker()
    result = worker.get_display_name(False, True, False)
    assert result == ""


def test_get_pwd():
    """Testing Worker.get_display_name() method."""
    from DisplayCAL.worker import Worker
    from DisplayCAL.config import initcfg

    initcfg()
    worker = Worker()
    test_value = "test_value"
    worker.pwd = test_value
    assert worker.pwd == test_value


def test_update_profile_1(random_icc_profile):
    """Testing Worker.update_profile() method."""
    from DisplayCAL import worker
    from DisplayCAL.worker import Worker
    from DisplayCAL.config import initcfg

    worker.dbus_session = None
    worker.dbus_system = None
    initcfg()
    worker = Worker()

    icc_profile, icc_profile_path = random_icc_profile
    with check_call_str(
        "DisplayCAL.worker.Worker.get_display_edid", DisplayData.DISPLAY_DATA_2
    ):
        worker.update_profile(icc_profile_path, tags=True)


def test_exec_cmd_1():
    """Test worker.exec_cmd() function for issue #73"""
    # Command line:
    from DisplayCAL.worker import Worker

    cmd = "/home/eoyilmaz/.local/bin/Argyll_V2.3.0/bin/colprof"
    args = [
        "-v",
        "-qh",
        "-ax",
        "-bn",
        "-C",
        b"No copyright. Created with DisplayCAL 3.8.9.3 and Argyll CMS 2.3.0",
        "-A",
        "Dell, Inc.",
        "-D",
        "UP2516D_#1_2022-04-01_00-26_2.2_F-S_XYZLUT+MTX",
        "/tmp/DisplayCAL-i91d9z8_/UP2516D_#1_2022-04-01_00-26_2.2_F-S_XYZLUT+MTX",
    ]
    cwd = "/tmp/DisplayCAL-i91d9z8_"
    worker = Worker()
    worker.exec_cmd(cmd=cmd, args=args)


def test_is_allowed_1():
    """Test Sudo.is_allowed() function for issue #76"""
    from DisplayCAL.worker import Sudo

    sudo = Sudo()
    result = sudo.is_allowed()
    assert result != ""


def test_ti3_lookup_to_ti1_1(data_files):
    """Test Worker.ti3_lookup_to_ti1() function for #129"""
    ti3_path = data_files["0_16_from_issue_129.ti3"].absolute()
    profile_path = data_files[
        "UP2516D #1 2022-03-23 16-06 D6500 2.2 F-S XYZLUT+MTX.icc"
    ].absolute()
    from DisplayCAL import CGATS, config, ICCProfile

    ti3_cgat = CGATS.CGATS(ti3_path)
    icc_profile = ICCProfile.ICCProfile(profile_path)
    config.initcfg()
    worker = Worker()
    ti1, ti3v = worker.ti3_lookup_to_ti1(ti3_cgat, icc_profile)
    assert isinstance(ti1, CGATS.CGATS)
    assert isinstance(ti3v, CGATS.CGATS)
    assert ti1 == {
            0: {
                "COLOR_REP": b"RGB",
                "DATA": {
                    0: {
                        "RGB_B": 99.9959,
                        "RGB_G": 100.0,
                        "RGB_R": 97.1526,
                        "SAMPLE_ID": 1,
                        "XYZ_X": 95.0104,
                        "XYZ_Y": 100.0,
                        "XYZ_Z": 92.7202,
                    },
                    1: {
                        "RGB_B": 9.1428,
                        "RGB_G": 5.8338,
                        "RGB_R": 5.842,
                        "SAMPLE_ID": 2,
                        "XYZ_X": 0.277593,
                        "XYZ_Y": 0.255279,
                        "XYZ_Z": 0.423145,
                    },
                    2: {
                        "RGB_B": 11.6181,
                        "RGB_G": 9.1081,
                        "RGB_R": 8.0801,
                        "SAMPLE_ID": 3,
                        "XYZ_X": 0.51238,
                        "XYZ_Y": 0.536117,
                        "XYZ_Z": 0.705578,
                    },
                },
                "DATA_FORMAT": {
                    0: b"SAMPLE_ID",
                    1: b"RGB_R",
                    2: b"RGB_G",
                    3: b"RGB_B",
                    4: b"XYZ_X",
                    5: b"XYZ_Y",
                    6: b"XYZ_Z",
                },
                "DESCRIPTOR": b"Argyll Calibration Target chart information 1",
                "KEYWORDS": {0: b"COLOR_REP"},
                "NUMBER_OF_FIELDS": None,
                "NUMBER_OF_SETS": None,
            }
        }

    assert ti3v == {
            "COLOR_REP": b"RGB_XYZ",
            "CREATED": b"Sun Jun  5 13:08:54 2022",
            "DATA": {
                0: {
                    "RGB_B": 99.9959,
                    "RGB_G": 100.0,
                    "RGB_R": 97.1526,
                    "SAMPLE_ID": 1,
                    "XYZ_X": 95.0104,
                    "XYZ_Y": 100.0,
                    "XYZ_Z": 92.7202,
                },
                1: {
                    "RGB_B": 9.1428,
                    "RGB_G": 5.8338,
                    "RGB_R": 5.842,
                    "SAMPLE_ID": 2,
                    "XYZ_X": 0.277593,
                    "XYZ_Y": 0.255279,
                    "XYZ_Z": 0.423145,
                },
                2: {
                    "RGB_B": 11.6181,
                    "RGB_G": 9.1081,
                    "RGB_R": 8.0801,
                    "SAMPLE_ID": 3,
                    "XYZ_X": 0.51238,
                    "XYZ_Y": 0.536117,
                    "XYZ_Z": 0.705578,
                },
            },
            "DATA_FORMAT": {
                0: b"SAMPLE_ID",
                1: b"RGB_R",
                2: b"RGB_G",
                3: b"RGB_B",
                4: b"XYZ_X",
                5: b"XYZ_Y",
                6: b"XYZ_Z",
            },
            "DESCRIPTOR": b"Argyll Calibration Target chart information 3",
            "DEVICE_CLASS": b"DISPLAY",
            "DISPLAY_TYPE_BASE_ID": 1,
            "DISPLAY_TYPE_REFRESH": b"NO",
            "INSTRUMENT_TYPE_SPECTRAL": b"NO",
            "LUMINANCE_XYZ_CDM2": b"42.204124 44.420532 41.186805",
            "NORMALIZED_TO_Y_100": b"YES",
            "NUMBER_OF_FIELDS": None,
            "NUMBER_OF_SETS": None,
            "ORIGINATOR": b"Argyll dispread",
            "TARGET_INSTRUMENT": b"Datacolor Spyder3",
            "VIDEO_LUT_CALIBRATION_POSSIBLE": b"YES",
        }
