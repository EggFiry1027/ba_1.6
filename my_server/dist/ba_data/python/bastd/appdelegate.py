# Released under the MIT License. See LICENSE for details.
#
"""Provide our delegate for high level app functionality."""
from __future__ import annotations

from typing import TYPE_CHECKING

import ba

if TYPE_CHECKING:
    from typing import Type, Any, Dict, Callable, Optional


class AppDelegate(ba.AppDelegate):
    """Defines handlers for high level app functionality."""

    def create_default_game_settings_ui(
            self, gameclass: Type[ba.GameActivity],
            sessiontype: Type[ba.Session], settings: Optional[dict],
            completion_call: Callable[[Optional[dict]], Any]) -> None:
        """(internal)"""

        # Replace the main window once we come up successfully.
        from bastd.ui.playlist.editgame import PlaylistEditGameWindow
        ba.app.ui.clear_main_menu_window(transition='out_left')
        ba.app.ui.set_main_menu_window(
            PlaylistEditGameWindow(
                gameclass,
                sessiontype,
                settings,
                completion_call=completion_call).get_root_widget())
