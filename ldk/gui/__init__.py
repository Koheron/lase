# __init__.py

from .cursor_widget import CursorWidget
from .dac_widget import DacWidget
from .lase_widget import LaseWidget
from .slider_widget import SliderWidget
from .oscillo_widget import OscilloWidget
from .laser_widget import LaserWidget
from .math_widget import MathWidget
from .monitor_widget import MonitorWidget
from .select_channel_widget import SelectChannelWidget
from .welcome_widget import WelcomeWidget
from .spectrum_widget import SpectrumWidget
from .stats_widget import StatsWidget

__all__ = ['CursorWidget',
           'DacWidget',
           'LaseWidget',
           'SliderWidget',
           'OscilloWidget',
           'LaserWidget',
           'MathWidget',
           'MonitorWidget',
           'SelectChannelWidget',
           'WelcomeWidget',
           'SpectrumWidget',
           'StatsWidget'
          ]
