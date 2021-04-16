# Released under the MIT License. See LICENSE for details.
#
"""Functionality related to the co-op join screen."""

from __future__ import annotations

from typing import TYPE_CHECKING

import _ba
import ba
from ba.internal import JoinActivity

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Sequence, Union


class CoopJoinActivity(JoinActivity):
    """Join-screen for co-op mode."""

    # We can assume our session is a CoopSession.
    session: ba.CoopSession

    def __init__(self, settings: dict):
        super().__init__(settings)
        session = self.session
        assert isinstance(session, ba.CoopSession)

        # Let's show a list of scores-to-beat for 1 player at least.
        assert session.campaign is not None
        level_name_full = (session.campaign.name + ':' +
                           session.campaign_level_name)
        config_str = ('1p' + session.campaign.getlevel(
            session.campaign_level_name).get_score_version_string().replace(
                ' ', '_'))
        _ba.get_scores_to_beat(level_name_full, config_str,
                               ba.WeakCall(self._on_got_scores_to_beat))

    def on_transition_in(self) -> None:
        from bastd.actor.controlsguide import ControlsGuide
        from bastd.actor.text import Text
        super().on_transition_in()
        assert isinstance(self.session, ba.CoopSession)
        assert self.session.campaign
        Text(self.session.campaign.getlevel(
            self.session.campaign_level_name).displayname,
             scale=1.3,
             h_attach=Text.HAttach.CENTER,
             h_align=Text.HAlign.CENTER,
             v_attach=Text.VAttach.TOP,
             transition=Text.Transition.FADE_IN,
             transition_delay=4.0,
             color=(1, 1, 1, 0.6),
             position=(0, -95)).autoretain()
        ControlsGuide(delay=1.0).autoretain()

    def _on_got_scores_to_beat(self,
                               scores: Optional[List[Dict[str, Any]]]) -> None:
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        from efro.util import asserttype
        from bastd.actor.text import Text

        # Sort by originating date so that the most recent is first.
        if scores is not None:
            scores.sort(reverse=True,
                        key=lambda score: asserttype(score['time'], int))

        # We only show achievements and challenges for CoopGameActivities.
        session = self.session
        assert isinstance(session, ba.CoopSession)
        gameinstance = session.get_current_game_instance()
        if isinstance(gameinstance, ba.CoopGameActivity):
            score_type = gameinstance.get_score_type()
            if scores is not None:
                achievement_challenges = [
                    a for a in scores if a['type'] == 'achievement_challenge'
                ]
                score_challenges = [
                    a for a in scores if a['type'] == 'score_challenge'
                ]
            else:
                achievement_challenges = score_challenges = []

            delay = 1.0
            vpos = -140.0
            spacing = 25
            delay_inc = 0.1

            def _add_t(
                text: Union[str, ba.Lstr],
                h_offs: float = 0.0,
                scale: float = 1.0,
                color: Sequence[float] = (1.0, 1.0, 1.0, 0.46)
            ) -> None:
                Text(text,
                     scale=scale * 0.76,
                     h_align=Text.HAlign.LEFT,
                     h_attach=Text.HAttach.LEFT,
                     v_attach=Text.VAttach.TOP,
                     transition=Text.Transition.FADE_IN,
                     transition_delay=delay,
                     color=color,
                     position=(60 + h_offs, vpos)).autoretain()

            if score_challenges:
                _add_t(ba.Lstr(value='${A}:',
                               subs=[('${A}',
                                      ba.Lstr(resource='scoreChallengesText'))
                                     ]),
                       scale=1.1)
                delay += delay_inc
                vpos -= spacing
                for chal in score_challenges:
                    _add_t(str(chal['value'] if score_type == 'points' else ba.
                               timestring(int(chal['value']) * 10,
                                          timeformat=ba.TimeFormat.MILLISECONDS
                                          ).evaluate()) + '  (1 player)',
                           h_offs=30,
                           color=(0.9, 0.7, 1.0, 0.8))
                    delay += delay_inc
                    vpos -= 0.6 * spacing
                    _add_t(chal['player'],
                           h_offs=40,
                           color=(0.8, 1, 0.8, 0.6),
                           scale=0.8)
                    delay += delay_inc
                    vpos -= 1.2 * spacing
                vpos -= 0.5 * spacing

            if achievement_challenges:
                _add_t(ba.Lstr(
                    value='${A}:',
                    subs=[('${A}',
                           ba.Lstr(resource='achievementChallengesText'))]),
                       scale=1.1)
                delay += delay_inc
                vpos -= spacing
                for chal in achievement_challenges:
                    _add_t(str(chal['value']),
                           h_offs=30,
                           color=(0.9, 0.7, 1.0, 0.8))
                    delay += delay_inc
                    vpos -= 0.6 * spacing
                    _add_t(chal['player'],
                           h_offs=40,
                           color=(0.8, 1, 0.8, 0.6),
                           scale=0.8)
                    delay += delay_inc
                    vpos -= 1.2 * spacing
                vpos -= 0.5 * spacing

            # Now list our remaining achievements for this level.
            assert self.session.campaign is not None
            assert isinstance(self.session, ba.CoopSession)
            levelname = (self.session.campaign.name + ':' +
                         self.session.campaign_level_name)
            ts_h_offs = 60

            if not (ba.app.demo_mode or ba.app.arcade_mode):
                achievements = [
                    a
                    for a in ba.app.ach.achievements_for_coop_level(levelname)
                    if not a.complete
                ]
                have_achievements = bool(achievements)
                achievements = [a for a in achievements if not a.complete]
                vrmode = ba.app.vr_mode
                if have_achievements:
                    Text(ba.Lstr(resource='achievementsRemainingText'),
                         host_only=True,
                         position=(ts_h_offs - 10, vpos),
                         transition=Text.Transition.FADE_IN,
                         scale=1.1 * 0.76,
                         h_attach=Text.HAttach.LEFT,
                         v_attach=Text.VAttach.TOP,
                         color=(1, 1, 1.2, 1) if vrmode else (0.8, 0.8, 1, 1),
                         shadow=1.0,
                         flatness=1.0 if vrmode else 0.6,
                         transition_delay=delay).autoretain()
                    hval = ts_h_offs + 50
                    vpos -= 35
                    for ach in achievements:
                        delay += 0.05
                        ach.create_display(hval, vpos, delay, style='in_game')
                        vpos -= 55
                    if not achievements:
                        Text(ba.Lstr(resource='noAchievementsRemainingText'),
                             host_only=True,
                             position=(ts_h_offs + 15, vpos + 10),
                             transition=Text.Transition.FADE_IN,
                             scale=0.7,
                             h_attach=Text.HAttach.LEFT,
                             v_attach=Text.VAttach.TOP,
                             color=(1, 1, 1, 0.5),
                             transition_delay=delay + 0.5).autoretain()
