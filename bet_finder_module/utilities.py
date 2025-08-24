
from enum import IntEnum

class CsvKeys(IntEnum):
    NO = 0
    SEASON = 1
    GAME_TYPE = 2
    DATE_ID = 3
    DATE = 4
    TEAM_RANK = 5
    TEAM = 6
    TEAM_CONF = 7
    TEAM_DIVISION = 8
    COACH = 9
    TEAM_SPREAD = 10
    SITE = 11
    OPP_RANK = 12
    OPPONENT = 13
    OPP_CONF = 14
    OPP_DIVISION = 15
    OPP_COACH = 16
    OPP_SPREAD = 17
    RESULT = 18
    TEAM_POINTS = 19
    OPP_POINTS = 20
    POINTS_DIFF = 21
    TOTAL_POINTS = 22
    TEAM_SEASON_ID = 23
    TEAM_VS_TEAM = 24
    COACH_VS_COACH = 25
    COACH_VS_TEAM = 26
    TEAM_GAME_NO = 27
    UNDERDOG_FAVORITE = 28
    COVERED = 29
    TEAM_WINS_ENTERING = 30
    TEAM_LOSSES_ENTERING = 31
    TEAM_TIES_ENTERING = 32
    TEAM_WIN_PCT_ENTERING = 33
    OPP_WINS_ENTERING = 34
    OPP_LOSSES_ENTERING = 35
    OPP_TIES_ENTERING = 36
    OPP_WIN_PCT_ENTERING = 37
    OVER_UNDER = 38
    OVER_OR_UNDER_RESULT = 39
    SCHEDULE_ID = 40
    GAME_TEAM_ID = 41
    EVENT_ID = 42


# Here are some imports that are useful
nfl_tricodes = {'49ers': 'SF', 'Bears': 'CHI', 'Bengals': 'CIN',
            'Bills': 'BUF', 'Broncos': 'DEN', 'Browns': 'CLE',
            'Buccaneers': 'TB', 'Cardinals': 'ARI', 'Chargers': 'LAC',
            'Chiefs': 'KC', 'Colts': 'IND', 'Cowboys': 'DAL',
            'Dolphins': 'MIA', 'Eagles': 'PHI', 'Falcons': 'ATL',
            'Giants': 'NYG', 'Jaguars': 'JAX', 'Jets': 'NYJ',
            'Lions': 'DET', 'Packers': 'GB', 'Panthers': 'CAR',
            'Patriots': 'NE', 'Raiders': 'LV', 'Rams': 'LAR',
            'Ravens': 'BAL', 'Saints': 'NO', 'Seahawks': 'SEA', 'Steelers': 'PIT',
            'Texans': 'HOU', 'Titans': 'TEN', 'Vikings': 'MIN', 'Washington': 'WAS'
            }


# Master dictionary: Team -> [Abbreviations]
cfb_tricodes = {
    # ACC
    "Boston College": ["BC"],
    "Clemson": ["CLEM"],
    "Duke": ["DUKE"],
    "Florida State": ["FSU"],
    "Georgia Tech": ["GT"],
    "Louisville": ["LOU"],
    "Miami": ["MIA"],
    "NC State": ["NCST"],
    "Pittsburgh": ["PITT"],
    "Syracuse": ["SYR"],
    "North Carolina": ["UNC"],
    "Virginia": ["UVA"],
    "Virginia Tech": ["VT"],
    "Wake Forest": ["WAKE"],

    # B1G
    "Illinois": ["ILL"],
    "Indiana": ["IND"],
    "Iowa": ["IOWA"],
    "Michigan": ["MICH"],
    "Michigan State": ["MSU"],
    "Minnesota": ["MINN"],
    "Nebraska": ["NEB"],
    "Northwestern": ["NW"],
    "Ohio State": ["OSU"],
    "Penn State": ["PSU"],
    "Purdue": ["PUR"],
    "Rutgers": ["RUTG"],
    "Maryland": ["UMD"],
    "Wisconsin": ["WIS"],

    # Big 12
    "Baylor": ["BAY"],
    "Iowa State": ["ISU"],
    "Kansas": ["KU"],
    "Kansas State": ["KSU"],
    "Oklahoma": ["OKLA", "OU"],
    "Oklahoma State": ["OKST"],
    "TCU": ["TCU"],
    "Texas": ["TEX"],
    "Texas Tech": ["TTU"],
    "West Virginia": ["WVU"],

    # Pac-12
    "Arizona": ["ARIZ"],
    "Arizona State": ["ASU"],
    "California": ["CAL"],
    "Colorado": ["COLO"],
    "Oregon": ["ORE", "UO"],
    "Oregon State": ["ORST"],
    "Stanford": ["STAN"],
    "UCLA": ["UCLA"],
    "USC": ["USC"],
    "Utah": ["UTAH"],
    "Washington": ["WASH", "UW"],
    "Washington State": ["WSU"],

    # SEC
    "Alabama": ["ALA", "BAMA"],
    "Arkansas": ["ARK"],
    "Auburn": ["AUB"],
    "Florida": ["FLA", "UF"],
    "Georgia": ["UGA"],
    "Kentucky": ["UK"],
    "LSU": ["LSU"],
    "Ole Miss": ["MISS"],
    "Mississippi State": ["MSST"],
    "Missouri": ["MIZ", "MIZZ"],
    "South Carolina": ["SC", "SCAR"],
    "Tennessee": ["TENN"],
    "Texas A&M": ["TAMU"],
    "Vanderbilt": ["VAN"],

    # Independents
    "BYU": ["BYU"],
    "Army": ["ARMY"],
    "UMass": ["UMASS"],
    "Notre Dame": ["ND"],

    # AAC
    "Cincinnati": ["CIN"],
    "UConn": ["CONN"],
    "East Carolina": ["ECU"],
    "Houston": ["HOU"],
    "Memphis": ["MEM"],
    "Navy": ["NAVY"],
    "SMU": ["SMU"],
    "South Florida": ["USF"],
    "Temple": ["TEM"],
    "Tulane": ["TULN"],
    "Tulsa": ["TLSA"],
    "Florida Atlantic": ["FAU"],
    "UCF": ["UCF"],
    "UAB": ["UAB"],

    # C-USA
    "Charlotte": ["CHAR"],
    "Florida International": ["FIU"],
    "Louisiana Tech": ["LT"],
    "Marshall": ["MRSH"],
    "Middle Tennessee": ["MTSU"],
    "North Texas": ["UNT"],
    "Old Dominion": ["ODU"],
    "Rice": ["RICE"],
    "Southern Miss": ["USM"],
    "UTEP": ["UTEP"],
    "UTSA": ["UTSA"],
    "Western Kentucky": ["WKU"],

    # MAC
    "Akron": ["AKR"],
    "Ball State": ["BALL"],
    "Bowling Green": ["BGSU"],
    "Buffalo": ["BUFF"],
    "Central Michigan": ["CMU"],
    "Eastern Michigan": ["EMU"],
    "Kent State": ["KENT"],
    "Miami (OH)": ["M-OH"],
    "Northern Illinois": ["NIU"],
    "Ohio": ["OHIO"],
    "Toledo": ["TOL", "TOLEDO"],
    "Western Michigan": ["WMU"],

    # Mountain West
    "Air Force": ["AFA"],
    "Boise State": ["BSU"],
    "Colorado State": ["CSU"],
    "Fresno State": ["FRES"],
    "Hawai'i": ["HAW"],
    "Nevada": ["NEV"],
    "New Mexico": ["UNM"],
    "San Diego State": ["SDSU"],
    "San Jose State": ["SJSU"],
    "UNLV": ["UNLV"],
    "Utah State": ["USU"],
    "Wyoming": ["WYO"],

    # Sun Belt
    "Appalachian State": ["APP"],
    "Arkansas State": ["ARST"],
    "Georgia Southern": ["GASO"],
    "Georgia State": ["GAST", "GSU"],
    "Idaho": ["IDHO"],
    "Louisiana Lafayette": ["ULL"],
    "UL Monroe": ["ULM"],
    "Louisiana": ["UL"],
    "New Mexico State": ["NMSU"],
    "South Alabama": ["USA"],
    "Texas State": ["TXST"],
    "Troy": ["TROY"],

    # Big Sky
    "Cal Poly": ["CP"],
    "Eastern Washington": ["EWU"],
    "Idaho State": ["IDST"],
    "Montana": ["MONT"],
    "Montana State": ["MTST"],
    "North Dakota": ["UND"],
    "Northern Arizona": ["NAU"],
    "Northern Colorado": ["UNCO"],
    "Portland State": ["PRST"],
    "Sacramento State": ["SAC"],
    "Southern Utah": ["SUU"],
    "UC Davis": ["UCD"],
    "Weber State": ["WEB"],

    # Big South
    "Charleston Southern": ["CHSO"],
    "Coastal Carolina": ["CCAR"],
    "Gardner-Webb": ["WEBB"],
    "Kennesaw State": ["KENN"],
    "Liberty": ["LIB"],
    "Monmouth": ["MONM"],
    "Presbyterian": ["PRE"],

    # CAA
    "Albany": ["ALBY"],
    "Delaware": ["DEL"],
    "Elon": ["ELON"],
    "James Madison": ["JMU"],
    "Maine": ["MAINE", "MNE"],
    "New Hampshire": ["UNH"],
    "Rhode Island": ["URI"],
    "Richmond": ["RICH"],
    "Stony Brook": ["STON"],
    "Towson": ["TOWS"],
    "Villanova": ["NOVA"],
    "William & Mary": ["W&M"],

    # Ivy League
    "Brown": ["BRWN"],
    "Cornell": ["COR"],
    "Columbia": ["CLMB"],
    "Dartmouth": ["DART"],
    "Harvard": ["HARV"],
    "UPenn": ["PENN"],
    "Princeton": ["PRIN"],
    "Yale": ["YALE"],

    # MEAC
    "Bethune-Cookman": ["COOK"],
    "Delaware State": ["DSU"],
    "Florida A&M": ["FAMU"],
    "Hampton": ["HAMP"],
    "Howard": ["HOW"],
    "Morgan State": ["MORG"],
    "Norfolk State": ["NORF"],
    "North Carolina A&T": ["NCAT"],
    "NC Central": ["NCCU"],
    "Savannah State": ["SAV"],
    "South Carolina State": ["SCST"],

    # Missouri Valley
    "Illinois State": ["ILST"],
    "Indiana State": ["INST"],
    "Missouri State": ["MOST"],
    "North Dakota State": ["NDSU"],
    "Northern Iowa": ["UNI"],
    "South Dakota": ["SDAK"],
    "South Dakota State": ["SDSU"],
    "Southern Illinois": ["SIU"],
    "Western Illinois": ["WIU"],
    "Youngstown State": ["YSU"],

    # NEC
    "Bryant": ["BRY"],
    "Central Connecticut": ["CCSU"],
    "Duquesne": ["DUQ"],
    "Robert Morris (PA)": ["RMU"],
    "Sacred Heart": ["SHU"],
    "St. Francis (PA)": ["SFU"],
    "Wagner": ["WAG"],

    # Ohio Valley
    "Austin Peay": ["PEAY"],
    "Eastern Illinois": ["EIU"],
    "Eastern Kentucky": ["EKY"],
    "Jacksonville State": ["JVST"],
    "Murray State": ["MURR"],
    "Southeast Missouri": ["SEMO"],
    "Tennessee State": ["TNST"],
    "Tennessee Tech": ["TNTC"],
    "UT Martin": ["UTM"],

    # Patriot
    "Bucknell": ["BUCK"],
    "Colgate": ["COLG"],
    "Fordham": ["FOR"],
    "Georgetown": ["GTWN"],
    "Holy Cross": ["HC"],
    "Lafayette": ["LAF"],
    "Lehigh": ["LEH"],

    # Pioneer
    "Butler": ["BUT"],
    "Campbell": ["CAMP"],
    "Davidson": ["DAV"],
    "Dayton": ["DAY"],
    "Drake": ["DRKE"],
    "Jacksonville": ["JAC"],
    "Marist": ["MRST"],
    "Morehead State": ["MORE"],
    "San Diego": ["USD"],
    "Stetson": ["STET"],
    "Valparaiso": ["VALP"],

    # SoCon
    "Chattanooga": ["CHAT"],
    "ETSU": ["ETSU"],
    "Furman": ["FUR"],
    "Mercer": ["MER"],
    "Samford": ["SAM"],
    "The Citadel": ["CIT"],
    "VMI": ["VMI"],
    "Western Carolina": ["WCU"],
    "Wofford": ["WOF"],

    # Southland
    "Abilene Christian": ["ACU"],
    "Central Arkansas": ["UCA"],
    "Houston Baptist": ["HBU"],
    "Incarnate Word": ["IW"],
    "Lamar": ["LAM"],
    "McNeese State": ["MCNS"],
    "Nicholls State": ["NICH"],
    "Northwestern State": ["NWST"],
    "Sam Houston State": ["SHSU"],
    "Southeastern Louisiana": ["SELA"],
    "Stephen F. Austin": ["SFA"],

    # SWAC
    "Alabama A&M": ["AAMU"],
    "Alabama State": ["ALST"],
    "Alcorn State": ["ALCN"],
    "Arkansas-Pine Bluff": ["ARPB"],
    "Grambling State": ["GRAM"],
    "Jackson State": ["JKST"],
    "Mississippi Valley State": ["MVSU"],
    "Prairie View A&M": ["PV"],
    "Southern University": ["SOU"],
    "Texas Southern": ["TXSO"],
}

# Reverse mapping: Abbreviation -> Team

cfb_teams = {abbr: team for team, abbrs in cfb_tricodes.items() for abbr in abbrs}


