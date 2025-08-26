from typing import Optional
class CfbSchedule:
    def __init__(
        self,
        home_team_id: Optional[int] = None,
        away_team_id: Optional[int] = None,
        game_date: Optional[str] = None,
        week: Optional[int] = None,
        season: Optional[int] = None,
    ):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.game_date = game_date
        self.week = week
        self.season = season
    def to_db_tuple(self):
        return (
            self.home_team_id,
            self.away_team_id,
            self.game_date,
            self.week,
            self.season
        )
    def __repr__(self):
        return f"<CfbSchedule Week: {self.week}: {self.away_team_id} at {self.home_team_id} on {self.date} {self.season}>"

