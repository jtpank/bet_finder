from typing import Optional
class CfbGame:
    def __init__(
        self,
        team_id: Optional[int] = None,
        opponent_id: Optional[int] = None,
        season: Optional[int] = None,
        game_type: Optional[str] = None,
        date: Optional[str] = None,  # ISO string, e.g., '2025-09-01'
        team_rank: Optional[int] = None,
        team: Optional[str] = None,
        team_conf: Optional[str] = None,
        team_division: Optional[str] = None,
        coach: Optional[str] = None,
        team_spread: Optional[float] = None,
        site: Optional[str] = None,
        opp_rank: Optional[int] = None,
        opponent: Optional[str] = None,
        opp_conf: Optional[str] = None,
        opp_division: Optional[str] = None,
        opp_coach: Optional[str] = None,
        opp_spread: Optional[float] = None,
        result: Optional[str] = None,
        team_points: Optional[int] = None,
        opp_points: Optional[int] = None,
        points_diff: Optional[int] = None,
        total_points: Optional[int] = None,
        team_season_id: Optional[int] = None,
        team_game_no: Optional[int] = None,
        underdog_favorite: Optional[str] = None,
        covered: Optional[str] = None,
        team_wins_entering: Optional[int] = None,
        team_losses_entering: Optional[int] = None,
        team_ties_entering: Optional[int] = None,
        opp_wins_entering: Optional[int] = None,
        opp_losses_entering: Optional[int] = None,
        opp_ties_entering: Optional[int] = None,
        over_under: Optional[float] = None,
        over_or_under_result: Optional[str] = None,
    ):
        self.team_id = team_id
        self.opponent_id = opponent_id
        self.season = season
        self.game_type = game_type
        self.date = date
        self.team_rank = team_rank
        self.team = team
        self.team_conf = team_conf
        self.team_division = team_division
        self.coach = coach
        self.team_spread = team_spread
        self.site = site
        self.opp_rank = opp_rank
        self.opponent = opponent
        self.opp_conf = opp_conf
        self.opp_division = opp_division
        self.opp_coach = opp_coach
        self.opp_spread = opp_spread
        self.result = result
        self.team_points = team_points
        self.opp_points = opp_points
        self.points_diff = points_diff
        self.total_points = total_points
        self.team_season_id = team_season_id
        self.team_game_no = team_game_no
        self.underdog_favorite = underdog_favorite
        self.covered = covered
        self.team_wins_entering = team_wins_entering
        self.team_losses_entering = team_losses_entering
        self.team_ties_entering = team_ties_entering
        self.opp_wins_entering = opp_wins_entering
        self.opp_losses_entering = opp_losses_entering
        self.opp_ties_entering = opp_ties_entering
        self.over_under = over_under
        self.over_or_under_result = over_or_under_result
    def to_db_tuple(self):
        return (
            self.team_id,
            self.opponent_id,
            self.season,
            self.game_type,
            self.date,
            self.team_rank,
            self.team,
            self.team_conf,
            self.team_division,
            self.coach,
            self.team_spread,
            self.site,
            self.opp_rank,
            self.opponent,
            self.opp_conf,
            self.opp_division,
            self.opp_coach,
            self.opp_spread,
            self.result,
            self.team_points,
            self.opp_points,
            self.points_diff,
            self.total_points,
            self.team_season_id,
            self.team_game_no,
            self.underdog_favorite,
            self.covered,
            self.team_wins_entering,
            self.team_losses_entering,
            self.team_ties_entering,
            self.opp_wins_entering,
            self.opp_losses_entering,
            self.opp_ties_entering,
            self.over_under,
            self.over_or_under_result,
        )
    def __repr__(self):
        return f"<CfbGame {self.team} vs {self.opponent} on {self.date}>"