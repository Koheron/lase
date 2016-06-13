# __init__.py

from .calibration_widget import CalibrationWidget
from .cursor_widget import CursorWidget
from .dac_widget import DacWidget
from .base_widget import BaseWidget
from .slider_widget import SliderWidget
from .oscillo_widget import OscilloWidget
from .laser_widget import LaserWidget
from .math_widget import MathWidget
from .monitor_widget import MonitorWidget
from .select_channel_widget import SelectChannelWidget
from .welcome_widget import WelcomeWidget
from .spectrum_widget import SpectrumWidget
from .stats_widget import StatsWidget
from .save_widget import SaveWidget

__all__ = ['CalibrationWidget',
           'CursorWidget',
           'DacWidget',
           'BaseWidget',
           'SliderWidget',
           'OscilloWidget',
           'LaserWidget',
           'MathWidget',
           'MonitorWidget',
           'SelectChannelWidget',
           'WelcomeWidget',
           'SpectrumWidget',
           'StatsWidget',
           'SaveWidget'
          ]
