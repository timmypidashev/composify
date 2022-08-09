from distutils.util import run_2to3
from unittest.mock import patch

from src.gpm import run_as_module

@patch("builtins.print")
def test_run_as_module(mock_print):
    run_as_module()

    mock_print.assert_called_once()