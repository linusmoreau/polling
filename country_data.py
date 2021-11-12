from date_kit import Date
from base_ui import black, dark_grey, grey

specs = {
    'Austria': {
        'include': ['ÖVP', 'SPÖ', 'FPÖ', 'Gr\u00fcne', 'NEOS'],
        'key': ['firm', 'date', 'sample', 'method',
                'ÖVP', 'SPÖ', 'FPÖ', 'Gr\u00fcne', 'NEOS',
                'Other', 'lead', 'end'],
        'col': {'ÖVP': (99, 195, 208), 'SPÖ': (206, 0, 12), 'FPÖ': (0, 86, 162), 'Gr\u00fcne': (136, 182, 38),
                'NEOS': (232, 65, 136)},
        'gov': {'Government': ['ÖVP', 'Gr\u00fcne'], 'Opposition': ['SPÖ', 'FPÖ', 'NEOS']},
        'blocs': {'Progressive': ['SPÖ', 'Gr\u00fcne', 'NEOS'], 'Conservative': ['ÖVP', 'FPÖ']},
        'start': 0,
        'end_date': Date(2024, 9, 29),
        'toggle_seats': True,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Austrian_legislative_election&action=edit&section=3',
        'seats': 183,
        'divisor': 1,
        'bar': 0,
        'threshold': 4,
        'method': 'quotient'
    },
    'Brazil': {
        'key': ['firm', 'date', 'sample',
                'Bolsanaro (APB)', 'Lula (PT)', 'Moro (PODE)', 'Gomes (PDT)', 'Doria (PSDB)',
                'Leite (PSDB)', 'Mandetta (DEM)', 'Pancheco (DEM)',
                'Other', 'Undecided', 'lead', 'end'],
        'include': ['Bolsanaro (APB)', 'Lula (PT)', 'Gomes (PDT)', 'Doria (PSDB)', 'Moro (PODE)'],
        'zeros': ['Undecided'],
        'col': {'Bolsanaro (APB)': (0, 140, 0), 'Lula (PT)': (204, 0, 0), 'Haddad (PT)': (204, 0, 0),
                'Dino (PCdoB)': (163, 0, 0), 'Gomes (PDT)': (238, 100, 100), 'Boulos (PSOL)': (163, 0, 0),
                'Doria (PSDB)': (0, 95, 164), 'Amoedo (NOVO)': (240, 118, 42), 'Silva (REDE)': (46, 139, 87),
                'Moro (PODE)': (45, 169, 51), 'Huck': grey},
        'start': 0,
        'vlines': {Date(2021, 3, 8): "Lula cleared of charges"},
        'end_date': Date(2022, 10, 2),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2022_Brazilian_general_election&action=edit&section=3',
    },
    'Bulgaria': {
        'include': ['ITN', 'GERB', 'BSPzB', 'DB', 'DPS', 'IBG-NI', 'IMRO', 'Revival', 'PP', 'BP'],
        'key': ['firm', 'date', 'sample', 'turnout', 'Undecided',
                'ITN', 'GERB', 'BSPzB', 'DB', 'DPS', 'IBG-NI', 'IMRO', 'Revival', 'PP',
                'Other', 'None', 'lead', 'end'],
        'col': {'GERB': (0, 86, 167), 'ITN': (75, 185, 222), 'BSPzB': (219, 15, 40), 'DPS': (0, 96, 170),
                'DB': (0, 74, 128), 'IBG-NI': (91, 165, 70), 'BP': (1, 25, 59), 'Revival': (192, 159, 98),
                'BL': (243, 129, 20), 'RzB': (43, 74, 153), 'LSChSR': (241, 25, 40), 'PP': (3, 22, 143),
                'IMRO': black,
                'Nationalist': black},
        'blocs': {'Conservative': ['GERB'], 'Socialist': ['BSPzB'], 'Liberal': ['DPS'],
                  'Nationalist': ['Revival', 'IMRO', 'BP'],
                  'Populist': ['ITN', 'DB', 'IBG-NI', 'PP']},
        'start': 0,
        'end_date': Date(2021, 11, 14),
        'toggle_seats': True,
        'url': 'https://en.wikipedia.org/w/index.php?title=2021_Bulgarian_general_election&action=edit&section=10',
        'old_data': 'polling_data/old_bulgaria_polling.txt',
        'seats': 240,
        'method': 'remainder',
        'threshold': 4,
        'vlines': {Date(2021, 7, 11): "Parliamentary Election",
                   Date(2021, 4, 4): "Parliamentary Election"},
        'zeros': ['Undecided', 'None']
    },
    'Canada': {
        'key': ['firm', 'date', 'link',
                'CON', 'LIB', 'NDP', 'BQ', 'PPC', 'GRN',
                'Other', 'margin', 'size', 'method', 'lead'],
        'include': ['CON', 'LIB', 'NDP', 'BQ', 'GRN', 'PPC'],
        'col': {'CON': (100, 149, 237), 'LIB': (234, 109, 106), 'NDP': (244, 164, 96), 'BQ': (135, 206, 250),
                'GRN': (153, 201, 85), 'PPC': (131, 120, 158),
                'Government': (234, 109, 106), 'Opposition': (100, 149, 237)},
        'gov': {'Government': ['LIB'], 'Opposition': ['CON', 'NDP', 'BQ', 'GRN', 'PPC']},
        'blocs': {'Progressive': ['LIB', 'NDP', 'BQ', 'GRN'], 'Conservative': ['CON', 'PPC']},
        'start': -2,
        'vlines': {Date(2019, 10, 21): "General Election",
                   Date(2020, 8, 24): "O'Toole elected Conservative leader",
                   Date(2017, 10, 1): "Singh elected NDP leader",
                   Date(2017, 5, 27): "Scheer elected Conservative leader",
                   Date(2021, 9, 20): "General Election"},
        'end_date': Date(2025, 9, 20),
        'toggle_seats': True,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_45th_Canadian_federal_election&action=edit&section=1',
        'old_data': 'polling_data/old_canada_polling.txt'
    },
    'Chile': {
        'key': ['date', 'source', 'type',
                'Artes', 'Boric', 'Enriquez-Om.', 'Provoste', 'Parisi', 'Sichel', 'Kast',
                'Other', 'end'],
        'include': ['Boric', 'Narvaez', 'Maldonado', 'Provoste', 'Sichel', 'Kast',
                    'Jadue', 'Jiles', 'Briones', 'Desbordes', 'Parisi', 'Lavin', 'Matthei',
                    'Enriquez-Om.', 'Artes'],
        'col': {'Boric': (255, 20, 85), 'Narvaez': (237, 22, 36), 'Maldonado': (205, 92, 92),
                'Provoste': (30, 144, 255), 'Sichel': (0, 107, 176), 'Kast': (49, 68, 108),
                'Jadue': (178, 34, 34), 'Jiles': (255, 69, 0), 'Briones': (0, 191, 255), 'Desbordes': (2, 78, 154),
                'Parisi': (24, 22, 68), 'Lavin': (41, 57, 138), 'Matthei': (41, 57, 138),
                'Enriquez-Om.': (255, 20, 147), 'Artes': (204, 0, 0)},
        'zeros': ['Other'],
        'start': -1,
        'end_date': Date(2021, 12, 19),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2021_Chilean_presidential_election&action=edit&section=2',
        'old_data': 'polling_data/old_chile_polling.txt',
        'vlines': {Date(2021, 7, 18): 'Official Primaries'}
    },
    'Czechia': {
        'key': ['firm', 'date', 'size', 'turnout',
                'ANO', 'SPOLU', 'SPOLU', 'SPOLU', 'PaS', 'PaS', 'SPD', 'KSCM', 'CSSD', 'T-S',
                'T-S', 'Z', 'APB', 'VB', 'P',
                'Other', 'Lead', 'Govt.', 'Opp.'],
        'include': ['ANO', 'SPOLU', 'PaS', 'SPD', 'KSCM', 'CSSD', 'T-S', 'Z', 'APB', 'P'],
        'col': {'ANO': (38, 16, 96), 'SPOLU': (35, 44, 119), 'PaS': (0, 0, 0), 'SPD': (33, 117, 187),
                'KSCM': (204, 0, 0), 'CSSD': (236, 88, 0), 'T-S': (0, 150, 130), 'Z': (96, 180, 76),
                'P': (0, 51, 255), 'APB': (0, 45, 114),
                'Government': (38, 16, 96), 'Opposition': (0, 0, 0)},
        'gov': {'Government': ['ANO', 'KSCM', 'CSSD'],
                'Opposition': ['SPOLU', 'PaS', 'SPD', 'T-S', 'Z', 'P']},
        'end_date': Date(2025, 10, 9),
        'start': 0,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2021_Czech_legislative_election&action=edit&section=3',
        'toggle_seats': True,
        'seats': 200,
        'divisor': 1,
        'bar': 0,
        'threshold': 5,
        'method': 'quotient',
        'vlines': {Date(2021, 10, 9): 'Parliamentary elections'}
    },
    'Denmark': {
        'key': ['firm', 'date', 'sample',
                'A', 'V', 'O', 'B', 'F', '\u00d8', 'C', '\u00c5', 'D', 'I', 'P', 'K', 'E', 'G', 'M', 'Q',
                'Other', 'lead', 'red', 'blue', 'lead', 'end'],
        'include': ['A', 'V', 'O', 'B', 'F', '\u00d8', 'C', '\u00c5', 'D', 'I', 'P', 'K', 'E', 'G'],
        'col': {'A': (240, 77, 70), 'V': (0, 40, 131), 'O': (252, 208, 59), 'B': (229, 0, 125), 'F': (191, 3, 26),
                '\u00d8': (208, 0, 77), 'C': (0, 73, 49), '\u00c5': (0, 255, 0), 'D': (0, 80, 91),
                'I': (63, 178, 190),
                'P': (1, 152, 225), 'K': (255, 165, 0), 'E': (0, 66, 36), 'G': (128, 165, 26),
                'Red': (240, 77, 70), 'Blue': (0, 40, 131)},
        'blocs': {'Red': ['A', 'B', 'F', '\u00d8', '\u00c5', 'G'],
                  'Blue': ['V', 'O', 'C', 'D', 'I', 'P', 'K', 'E']},
        'start': 0,
        'end_date': Date(2023, 6, 4),
        'toggle_seats': True,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Danish_general_election&action=edit&section=3',
        'seats': 175,
        'divisor': 2,
        'bar': 0,
        'threshold': 2,
        'method': 'quotient',
        'old_data': 'polling_data/old_denmark_polling.txt'
    },
    'Estonia': {
        'key': ['firm', 'date', 'sample',
                'Reform', 'Centre', 'EKRE', 'Isamaa', 'SDE', 'E200', 'Green',
                'Other', 'lead', 'gov', 'opp', 'end'],
        'include': ['Reform', 'Centre', 'EKRE', 'Isamaa', 'SDE', 'E200', 'Green'],
        'col': {'Reform': (255, 226, 0), 'Centre': (0, 117, 87), 'EKRE': (0, 99, 175), 'Isamaa': (0, 156, 226),
                'SDE': (225, 6, 0), 'E200': (6, 119, 141), 'Green': (128, 187, 61)},
        'gov': {'Government': ['Reform', 'Centre'], 'Opposition': ['EKRE', 'Isamaa', 'SDE', 'E200', 'Green']},
        'blocs': {'Liberal': ['Reform', 'Centre', 'E200', 'Green'], 'Nationalist': ['EKRE', 'Isamaa'],
                  'Socialist': ['SDE']},
        'start': 0,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Estonian_parliamentary_election&action=edit&section=3',
        'old_data': 'polling_data/old_estonia_polling.txt',
        'end_date': Date(2023, 3, 5),
        'threshold': 5,
        'method': 'quotient',
        'bar': 0,
        'divisor': 1,
        'toggle_seats': True,
        'seats': 101
    },
    'Finland': {
        'key': ['firm', 'date', 'sample',
                'SDP', 'PS', 'KOK', 'KESK', 'VIHR', 'VAS', 'SFP', 'KD', 'LIIK',
                'Other', 'lead', 'gov', 'opp', 'end'],
        'include': ['SDP', 'PS', 'KOK', 'KESK', 'VIHR', 'VAS', 'SFP', 'KD', 'LIIK'],
        'col': {'SDP': (245, 75, 75), 'PS': (255, 222, 85), 'KOK': (0, 98, 136), 'KESK': (52, 154, 43),
                'VIHR': (97, 191, 26), 'VAS': (240, 10, 100), 'SFP': (255, 221, 147), 'KD': (2, 53, 164),
                'LIIK': (180, 31, 121),
                'Government': (245, 75, 75), 'Opposition': (255, 222, 85)},
        'gov': {'Government': ['SDP', 'KESK', 'VIHR', 'VAS', 'SFP'], 'Opposition': ['KOK', 'PS', 'KD', 'LIIK']},
        'start': 0,
        'restart': ['http'],
        'end_date': Date(2023, 4, 30),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Finnish_parliamentary_election&action=edit&section=3',
        'toggle_seats': True,
        'seats': 200,
        'divisor': 1,
        'bar': 0,
        'threshold': 2,
        'method': 'quotient'
    },
    'Germany': {
        'include': ['Union', 'SPD', 'AfD', 'FDP', 'Linke', 'Gr\u00fcne'],
        'key': ['firm', 'date', 'sample', 'abs',
                'SPD', 'Union', 'Gr\u00fcne', 'FDP', 'AfD', 'Linke',
                'Other', 'lead', 'end'],
        'col': {'Union': (0, 0, 0), 'Gr\u00fcne': (100, 161, 45), 'SPD': (235, 0, 31), 'FDP': (255, 237, 0),
                'AfD': (0, 158, 224), 'Linke': (190, 48, 117),
                'Red-Red-Green': (190, 48, 117), 'Black-Yellow': (255, 237, 0), 'Jamaica': (118, 132, 15),
                'Grand Coalition': (0, 0, 0), 'Traffic Light': (235, 0, 31), 'Black-Green': (100, 161, 45),
                'Old Guard': (245, 118, 15), 'Big Three': (0, 0, 180)},
        'blocs': {'Red-Red-Green': ['Gr\u00fcne', 'SPD', 'Linke'],
                  'Black-Yellow': ['Union', 'FDP'],
                  'Jamaica': ['Union', 'FDP', 'Gr\u00fcne'],
                  'Traffic Light': ['SPD', 'Gr\u00fcne', 'FDP'],
                  'Grand Coalition': ['Union', 'SPD'],
                  'Black-Green': ['Union', 'Gr\u00fcne'],
                  'Old Guard': ['Union', 'SPD', 'FDP'],
                  'Big Three': ['Union', 'SPD', 'Gr\u00fcne']},
        'gov': {'Government': ['Union', 'SPD'], 'Opposition': ['Gr\u00fcne', 'Linke', 'FDP', 'AfD']},
        'start': 0,
        'end_date': Date(2025, 9, 26),
        'vlines': {Date(2020, 9, 10): 'Scholz (SPD) Chancellor Candidate',
                   Date(2021, 4, 19): 'Laschet (Union) and Baerbock (Gr\u00fcne) Chancellor Candidates',
                   Date(2021, 9, 26): 'Parliamentary elections'},
        'toggle_seats': True,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_German_federal_election&action=edit&section=3',
        'seats': 598,
        'divisor': 2,
        'bar': 0,
        'threshold': 5,
        'method': 'quotient',
        'old_data': 'polling_data/old_germany_polling.txt'
    },
    'Greece': {
        'key': ['firm', 'date', 'sample',
                'ND', 'Syriza', 'KINAL', 'KKE', 'EL', 'MeRA25', 'XA', 'PE', 'ANT', 'EP',
                'lead', 'end'],
        'include': ['ND', 'Syriza', 'KINAL', 'KKE', 'EL', 'MeRA25'],
        'col': {'ND': (27, 92, 199), 'Syriza': (238, 128, 143), 'KINAL': (45, 144, 45), 'KKE': (227, 3, 1),
                'EL': (84, 147, 206), 'MeRA25': (195, 52, 29), 'XA': (0, 2, 45)},
        'gov': {'Government': ['ND'], 'Opposition': ['Syriza', 'KINAL', 'KKE', 'EL', 'MeRA25', 'XA']},
        'blocs': {'Right': ['ND', 'EL'], 'Left': ['Syriza', 'KINAL', 'KKE', 'MeRA25']},
        'end_date': Date(2023, 7, 7),
        'start': 0,
        'restart': ['http'],
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Greek_legislative_election&action=edit&section=3'
    },
    'Hungary': {
        'include': ['Fidesz', 'Jobbik', 'MSZP', 'Dialogue', 'DK', 'LMP', 'MM', 'MKKP', 'MHM'],
        'key': ['date', 'firm', 'sample',
                'Fidesz', 'Jobbik', 'MSZP', 'Dialogue', 'DK', 'LMP', 'MM', 'MKKP', 'MHM',
                'Other', 'lead', 'opposition', 'end'],
        'col': {'Fidesz': (255, 106, 0), 'Jobbik': (0, 131, 113), 'MSZP': (204, 0, 0), 'Dialogue': (60, 179, 77),
                'DK': (0, 103, 170), 'LMP': (54, 202, 139), 'MM': (142, 111, 206), 'MKKP': (128, 128, 128),
                'MHM': (86, 130, 3),
                'United Opposition': (32, 178, 170)},
        'blocs': {'Fidesz': ['Fidesz'], 'United Opposition': ['Jobbik', 'MSZP', 'Dialogue', 'DK', 'LMP', 'MM']},
        'date': 0,
        'start': -1,
        'end_date': Date(2022, 4, 8),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2022_Hungarian_parliamentary_election&action=edit&section=4'
    },
    'Iceland': {
        'include': ['D', 'V', 'S', 'M', 'B', 'P', 'F', 'C', 'J'],
        'key': ['firm', 'date', 'sample', 'resp',
                'D', 'V', 'S', 'M', 'B', 'P', 'F', 'C', 'J',
                'Other', 'lead', 'end'],
        'col': {'D': (0, 173, 239), 'V': (0, 184, 120), 'S': (234, 0, 56), 'M': (0, 33, 105), 'B': (160, 208, 103),
                'P': (137, 110, 189), 'F': (255, 202, 62), 'C': (255, 125, 20), 'J': (239, 72, 57),
                'Government': (0, 184, 120), 'Opposition': (234, 0, 56),
                'Socialist': (234, 0, 56), 'Liberal': (160, 208, 103), 'Conservative': (0, 173, 239)},
        'blocs': {'Socialist': ['V', 'S', 'J', 'F'], 'Liberal': ['B', 'C', 'P'], 'Conservative': ['D', 'M']},
        'gov': {'Government': ['V', 'B', 'D'], 'Opposition': ['S', 'M', 'P', 'F', 'C', 'J']},
        'start': 0,
        'end_date': Date(2025, 9, 25),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2021_Icelandic_parliamentary_election&action=edit&section=2',
        'toggle_seats': True,
        'divisor': 1,
        'bar': 0,
        'method': 'quotient',
        'threshold': 5,
        'seats': 63,
        'vlines': {Date(2021, 9, 25): "Parliamentary elections"}
    },
    'Israel': {
        'key': ['date', 'firm', 'publisher',
                'Likud', 'Yesh Atid', 'Shas', 'Blue & White', 'Yamina', 'Labor', 'UTJ', 'Yisrael Beitenu',
                'Religious Zionist', 'Joint List', 'New Hope', 'Meretz', 'Ra\'am',
                'gov', 'end'],
        'include': ['Likud', 'Yesh Atid', 'Shas', 'Blue & White', 'Yamina', 'Labor', 'UTJ', 'Yisrael Beitenu',
                    'Religious Zionist', 'Joint List', 'New Hope', 'Meretz', 'Ra\'am'],
        'col': {'Likud': (31, 90, 165), 'Yesh Atid': (0, 59, 163), 'Shas': (0, 0, 0), 'Blue & White': (4, 190, 239),
                'Yamina': (25, 163, 189), 'Labor': (238, 28, 37), 'UTJ': (0, 51, 102),
                'Yisrael Beitenu': (154, 192, 226), 'Religious Zionist': (0, 113, 173), 'Joint List': (1, 178, 172),
                'New Hope': (0, 129, 178), 'Meretz': (64, 174, 73), 'Ra\'am': (21, 121, 61),
                'Opposition': (0, 0, 0)},
        'gov': {'Government': ['Yesh Atid', 'Blue & White', 'Yamina', 'Labor', 'Yisrael Beitenu', 'New Hope',
                               'Meretz', 'Ra\'am'],
                'Opposition': ['Likud', 'Shas', 'UTJ', 'Religious Zionist', 'Joint List']},
        'blocs': {'Centre': ['Yesh Atid', 'Blue & White'],
                  'Secular Right': ['Likud', 'Yamina', 'Yisrael Beitenu', 'New Hope'],
                  'Religious Right': ['Shas', 'UTJ', 'Religious Zionist', 'Ra\'am'],
                  'Left': ['Labor', 'Meretz', 'Joint List']},
        'start': -2,
        'restart': ['cite news', 'Cite news'],
        'end_date': Date(2025, 11, 11),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Israeli_legislative_election&action=edit&section=3',
        'toggle_seats': True,
        'method': 'quotient',
        'divisor': 1,
        'bar': 0,
        'threshold': 3.25,
        'seats': 120
    },
    'Ireland': {
        'include': ['SF', 'FF', 'FG', 'GP', 'Lab', 'SD', 'PBP/S', 'Aon', 'O/I'],
        'key': ['date', 'firm', 'sample',
                'SF', 'FF', 'FG', 'GP', 'Lab', 'SD', 'PBP/S', 'Aon', 'O/I',
                'end'],
        'col': {'SF': (50, 103, 96), 'FF': (102, 187, 102), 'FG': (102, 153, 255), 'GP': (34, 172, 111),
                'Lab': (204, 0, 0), 'SD': (117, 47, 139), 'PBP/S': (142, 36, 32), 'Aon': (68, 83, 42), 'O/I': grey},
        'blocs': {'Broad Left': ['SF', 'GP', 'Lab', 'SD', 'PBP/S'], 'Old Guard': ['FF', 'FG']},
        'gov': {'Government': ['FF', 'FG', 'GP'], 'Opposition': ['SF', 'Lab', 'SD', 'PBP/S', 'Aon', 'O/I']},
        'start': -1,
        'restart': ['Cite', 'cite'],
        'vlines': {Date(2020, 2, 8): 'General Election'},
        'end_date': Date(2025, 2, 20),
        'old_data': 'polling_data/old_ireland_polling.txt',
        'url': 'https://en.wikipedia.org/w/index.php?title=Next_Irish_general_election&action=edit&section=3'
    },
    'Italy': {
        'key': ['date', 'firm', 'sample',
                'M5S', 'PD', 'Lega', 'FI', 'FdI', 'Art.1', 'SI', '+Eu', 'EV', 'A', 'IV', 'CI',
                'Other', 'lead', 'end'],
        'include': ['M5S', 'PD', 'Lega', 'FI', 'FdI', 'Art.1', 'SI', '+Eu', 'EV', 'A', 'IV', 'CI', 'PaP', 'NcI',
                    'LeU', 'C!'],
        'col': {'M5S': (255, 235, 59), 'PD': (239, 28, 39), 'Lega': (0, 128, 0), 'FI': (0, 135, 220),
                'FdI': (3, 56, 106), 'LeU': (199, 40, 55), '+Eu': (255, 215, 0), 'EV': (115, 193, 112),
                'C!': (229, 131, 33), 'A': (0, 57, 170), 'IV': (214, 65, 140), 'NcI': (31, 107, 184),
                'PaP': (160, 20, 46), 'Art.1': (210, 27, 48), 'SI': (239, 62, 62), 'CI': (49, 39, 131),
                'Left': (239, 28, 39), 'Right': (0, 128, 0),
                'Government': (255, 235, 59), 'Opposition': (3, 56, 106)},
        'blocs': {'Left': ['PD', '+Eu', 'EV', 'LeU', 'IV', 'A', 'M5S', 'PaP', 'Art.1', 'SI'],
                  'Right': ['Lega', 'FI', 'FdI', 'C!', 'NcI', 'CI']},
        'gov': {'Government': ['M5S', 'Lega', 'PD', 'FI', 'LeU', 'IV', 'Art.1'],
                'Opposition': ['FdI', '+Eu', 'C!', 'A', 'SI', 'CI']},
        'start': -1,
        'end_date': Date(2023, 6, 1),
        'old_data': 'polling_data/old_italy_polling.txt',
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Italian_general_election&action=edit&section=3'
    },
    'Japan': {
        'key': ['date', 'firm',
                'LDP', 'CDP', 'NKP', 'JCP', 'Ishin', 'DPP', 'SDP', 'Reiwa', 'NHK',
                'Other', 'None', 'lead', 'end'],
        'include': ['LDP', 'CDP', 'NKP', 'JCP', 'Ishin', 'DPP', 'SDP', 'Reiwa', 'NHK'],
        'gov': {'Government': ['LDP', 'NKP'],
                'Opposition': ['CDP', 'JCP', 'Ishin', 'DPP', 'SDP', 'Reiwa', 'NHK']},
        'zeros': ['None'],
        'col': {'LDP': (60, 163, 36), 'CDP': (24, 69, 137), 'NKP': (245, 88, 129), 'JCP': (219, 0, 28),
                'Ishin': (184, 206, 67), 'DPP': (255, 215, 0), 'SDP': (28, 169, 233), 'Reiwa': (237, 0, 140),
                'NHK': (248, 234, 13)},
        'start': -1,
        'end_date': Date(2021, 10, 31),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2021_Japanese_general_election&action=edit&section=9',
        'old_data': 'polling_data/old_japan_polling.txt',
        'vlines': {Date(2021, 9, 3): "PM Suga announces resignation"}
    },
    'Latvia': {
        'key': ['firm', 'date', 'sample', 'dec',
                'S', 'PCL', 'JKP', 'AP!', 'NA', 'ZZS', 'JV', 'LRA', 'LKS', 'P', 'LuK', 'LPV', 'R',
                'Other', 'lead', 'gov', 'opp', 'end'],
        'include': ['S', 'PCL', 'JKP', 'AP!', 'NA', 'ZZS', 'JV', 'LRA', 'LKS', 'P', 'LuK', 'LPV', 'R'],
        'col': {'S': (238, 34, 43), 'PCL': (0, 172, 180), 'JKP': (24, 41, 86), 'AP!': (255, 221, 0),
                'NA': (147, 35, 48), 'ZZS': (2, 114, 58), 'JV': (106, 182, 71), 'LRA': (14, 50, 103),
                'LKS': (53, 96, 169), 'P': (230, 70, 50), 'LuK': (36, 28, 36), 'LPV': (158, 48, 57),
                'R': (27, 77, 125)},
        'gov': {'Government': ['JKP', 'AP!', 'NA', 'JV'],
                'Opposition': ['S', 'PCL', 'ZZS', 'LRA', 'LKS', 'P', 'LuK', 'LPV', 'R']},
        'blocs': {'Conservative': ['JKP', 'NA', 'PCL', 'ZZS', 'JV', 'LuK', 'LPV', 'R'],
                  'Socialist': ['S', 'P', 'LKS'],
                  'Liberal': ['LRA', 'AP!']},
        'zeros': ['Undecided', 'None'],
        'start': 0,
        'end_date': Date(2022, 9, 1),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2022_Latvian_parliamentary_election&action=edit&section=3',
        'toggle_seats': True,
        'seats': 100,
        'divisor': 2,
        'method': 'quotient',
        'threshold': 5,
        'bar': 0,
        'restart': ['Cite web', 'cite web']
    },
    'Lithuania': {
        'include': ['TS-LKD', 'LVZS', 'DP', 'LSDP', 'Laisves', 'LRLS', 'LLRA', 'LRP', 'LCP', 'LT'],
        'key': ['firm', 'date', 'sample',
                'TS-LKD', 'LVZS', 'DP', 'LSDP', 'Laisves', 'LRLS', 'LLRA', 'LRP', 'LCP', 'LT',
                'lead', 'end'],
        'col': {'TS-LKD': (0, 165, 155), 'LVZS': (0, 144, 53), 'DP': (29, 87, 140), 'LSDP': (225, 5, 20),
                'Laisves': (227, 0, 107), 'LRLS': (244, 129, 0), 'LLRA': (120, 19, 35), 'LRP': (193, 39, 45),
                'LCP': (0, 156, 61), 'LT': (251, 186, 0)},
        'gov': {'Government': ['TS-LKD', 'Laisves', 'LRLS'],
                'Opposition': ['LVZS', 'DP', 'LSDP', 'LLRA', 'LRP', 'LCP', 'LT']},
        'blocs': {'Conservative': ['TS-LKD', 'LVZS', 'LCP', 'LLRA'], 'Liberal': ['LRLS', 'DP', 'Laisves', 'LT'],
                  'Socialist': ['LSDP', 'LRP']},
        'start': 0,
        'end_date': Date(2024, 10, 6),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               '2024_Lithuanian_parliamentary_election&action=edit&section=2'
    },
    'Netherlands': {
        'key': ['firm', 'date', 'sample',
                'VVD', 'D66', 'PVV', 'CDA', 'SP', 'PvdA', 'GL', 'FVD', 'PvdD', 'CU', 'Volt', 'JA21', 'SGP', 'DENK',
                '50+', 'BBB', 'BIJ1',
                'Others', 'lead', 'end'],
        'col': {'VVD': (10, 44, 202), 'D66': (0, 174, 65), 'PVV': (1, 39, 88), 'CDA': (44, 200, 77),
                'SP': (246, 0, 0), 'PvdA': (223, 17, 26), 'GL': (131, 189, 0), 'FVD': (132, 24, 24),
                'PvdD': (0, 107, 45), 'CU': (0, 167, 235), 'Volt': (88, 44, 131), 'JA21': (36, 43, 87),
                'SGP': (234, 91, 11), 'DENK': (0, 183, 178), '50+': (146, 16, 125), 'BBB': (148, 193, 31),
                'BIJ1': (253, 253, 0)},
        'include': ['VVD', 'D66', 'PVV', 'CDA', 'SP', 'PvdA', 'GL', 'FVD', 'PvdD', 'CU', 'Volt', 'JA21', 'SGP',
                    'DENK', '50+', 'BBB', 'BIJ1'],
        'gov': {'Government': ['VVD', 'D66', 'CDA', 'CU'],
                'Opposition': ['PVV', 'SP', 'PvdA', 'GL', 'FVD', 'PvdD', 'Volt', 'JA21', 'SGP', 'DENK', '50+',
                               'BBB', 'BIJ1']},
        'blocs': {'Nationalist': ['PVV', 'FVD', 'JA21'],
                  'Confessional': ['CDA', 'CU', 'SGP'],
                  'Socialist': ['SP', 'PvdA', 'GL', 'PvdD', 'BIJ1', 'DENK'],
                  'Liberal': ['VVD', 'D66', 'Volt'],
                  'Agrarian': ['BBB'],
                  'Pensioners': ['50+']},
        'start': 0,
        'vlines': {Date(2021, 3, 17): 'General Election'},
        'url': 'https://en.wikipedia.org/w/index.php?title=Next_Dutch_general_election&action=edit&section=3',
        'old_data': 'polling_data/old_netherlands_polling.txt',
        'toggle_seats': True,
        'method': 'quotient',
        'bar': 0,
        'divisor': 1,
        'seats': 150,
        'threshold': 0,
        'end_date': Date(2025, 3, 17)
    },
    'Norway': {
        'include': ['R', 'SV', 'MDG', 'Ap', 'Sp', 'V', 'KrF', 'H', 'FrP'],
        'key': ['firm', 'date', 'sample', 'resp',
                'R', 'SV', 'MDG', 'Ap', 'Sp', 'V', 'KrF', 'H', 'FrP',
                'Other', 'lead', 'end'],
        'col': {'R': (231, 52, 69), 'SV': (188, 33, 73), 'MDG': (106, 147, 37), 'Ap': (227, 24, 54),
                'Sp': (0, 133, 66),
                'V': (17, 100, 104), 'KrF': (254, 193, 30), 'H': (135, 173, 215), 'FrP': (2, 76, 147),
                'Red-Green': (227, 24, 54), 'Blue': (135, 173, 215)},
        'blocs': {'Red-Green': ['Ap', 'SV', 'Sp'],
                  'Blue': ['V', 'KrF', 'H', 'FrP'],
                  'Socialist': ['R', 'SV', 'Ap', 'MDG'],
                  'Bourgeois': ['FrP', 'Sp', 'V', 'KrF', 'H'],
                  'Red-Green+': ['MDG', 'R', 'SV', 'Ap', 'Sp']},
        'start': 0,
        'end_date': Date(2025, 9, 13),
        'toggle_seats': True,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2025_Norwegian_parliamentary_election&action=edit&section=3',
        'seats': 169,
        'divisor': 2,
        'bar': 0.4,
        'threshold': 4,
        'method': 'quotient',
        'old_data': 'polling_data/old_norway_polling.txt',
        'vlines': {Date(2021, 9, 13): "General elections"}
    },
    'Ontario': {
        'include': ['PC', 'NDP', 'Liberal', 'Green'],
        'key': ['firm', 'date', 'source',
                'PC', 'NDP', 'Liberal', 'Green',
                'Other', 'type', 'sample', 'moe', 'lead', 'end'],
        'col': {'PC': (153, 153, 255), 'NDP': (244, 164, 96), 'Liberal': (234, 109, 106), 'Green': (153, 201, 85)},
        'start': -2,
        'end_date': Date(2022, 6, 2),
        'url': 'https://en.wikipedia.org/w/index.php?title=43rd_Ontario_general_election&action=edit&section=9'
    },
    'Poland': {
        'key': ['firm', 'date', 'sample',
                'United Right', 'Agreement', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Kukiz\'15',
                'Confederation', 'Poland 2050', 'AGRO unia',
                'Other', 'lead', 'end'],
        'include': ['United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Kukiz\'15', 'Confederation',
                    'Poland 2050'],
        'col': {'United Right': (38, 55, 120), 'Civic Coalition': (246, 143, 45), 'The Left': (172, 20, 90),
                'Polish Coalition': (27, 177, 0), 'Kukiz\'15': (0, 0, 0), 'Confederation': (18, 39, 70),
                'Poland 2050': (249, 192, 19),
                'Government': (38, 55, 120), 'Opposition': (246, 143, 45),
                'United Opposition': (246, 143, 45), 'Misc. Right': (18, 39, 70)},
        'gov': {'Government': ['United Right'],
                'Opposition': ['Civic Coalition', 'The Left', 'Polish Coalition', 'Kukiz\'15', 'Confederation',
                               'Poland 2050']},
        'blocs': {'United Right': ['United Right'],
                  'United Opposition': ['Civic Coalition', 'The Left', 'Polish Coalition', 'Poland 2050'],
                  'Misc. Right': ['Kukiz\'15', 'Confederation']},
        'start': 0,
        'end_date': Date(2023, 11, 11),
        'old_data': 'polling_data/old_poland_polling.txt',
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Polish_parliamentary_election&action=edit&section=3',
        'seats': 460,
        'method': 'quotient',
        'divisor': 1,
        'threshold': 5,
        'bar': 0,
        'toggle_seats': True
    },
    'Portugal': {
        'key': ['firm', 'date', 'sample', 'turnout',
                'PS', 'PSD', 'BE', 'CDU', 'CDS-PP', 'PAN', 'Chega', 'IL', 'LIVRE',
                'Other', 'lead', 'end'],
        'include': ['PS', 'PSD', 'BE', 'CDU', 'CDS-PP', 'PAN', 'Chega', 'IL', 'LIVRE'],
        'col': {'PS': (255, 102, 255), 'PSD': (255, 153, 0), 'BE': (139, 0, 0), 'CDU': (255, 0, 0),
                'CDS-PP': (0, 147, 221),
                'PAN': (0, 128, 128), 'Chega': (32, 32, 86), 'IL': (0, 173, 239), 'LIVRE': (143, 188, 143),
                'Left': (255, 102, 255), 'Right': (255, 153, 0)},
        'blocs': {'Left': ['PS', 'BE', 'CDU', 'PAN', 'LIVRE'], 'Right': ['PSD', 'CDS-PP', 'Chega', 'IL']},
        'start': 0,
        'end_date': Date(2022, 1, 30),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2022_Portuguese_legislative_election&action=edit&section=3',
        'toggle_seats': True,
        'seats': 200,
        'divisor': 1,
        'bar': 0,
        'threshold': 0,
        'method': 'quotient'
    },
    'Romania': {
        'key': ['date', 'source', 'sample',
                'PSD', 'PNL', 'USR', 'AUR', 'UDMR', 'PMP', 'PRO', 'ALDE', 'PPU-SL', 'PER', 'APP',
                'Other', 'lead', 'end'],
        'include': ['PSD', 'PNL', 'FL', 'USR', 'AUR', 'UDMR', 'PMP', 'PRO', 'ALDE', 'PPU-SL', 'PER'],
        'col': {'PSD': (237, 33, 40), 'PNL': (255, 221, 0), 'USR': (0, 166, 255), 'AUR': (252, 194, 36),
                'UDMR': (41, 102, 51), 'PMP': (167, 207, 53), 'PRO': (21, 114, 186), 'PPU-SL': (102, 204, 255),
                'PER': (0, 117, 58), 'ALDE': (0, 84, 135), 'FL': (255, 221, 147)},
        'gov': {'Government': ['PNL', 'USR', 'UDMR'],
                'Opposition': ['PSD', 'AUR', 'PMP', 'PRO', 'PPU-SL', 'ALDE', 'PER']},
        'end_date': Date(2025, 3, 25),
        'restart': ['[https', 'CURS'],
        'start': -1,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Romanian_legislative_election&action=edit&section=1',
    },
    'Russia': {
        'key': ['date', 'firm', 'sample', 'UR', 'CPRF', 'LDPR', 'SRZP', 'NP',
                'Others', 'Undecided', 'Abstention',
                'lead', 'end'],
        'col': {'UR': (46, 78, 164), 'CPRF': (204, 17, 17), 'LDPR': (68, 136, 204), 'SRZP': (255, 192, 3),
                'NP': (10, 209, 201)},
        'include': ['UR', 'CPRF', 'LDPR', 'SRZP', 'NP'],
        'zeros': ['Undecided', 'Abstention'],
        'start': -1,
        'end_date': Date(2026, 9, 20),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2026_Russian_legislative_election&action=edit&section=3',
        'old_data': 'polling_data/old_russia_polling.txt',
        'vlines': {Date(2018, 6, 14): 'Retirement Age Increase Announced',
                   Date(2021, 9, 19): 'Parliamentary elections'},
    },
    'Slovakia': {
        'include': ['OL\'aNO', 'SMER-SD', 'SR', 'L\'SNS', 'PS', 'SaS', 'ZL\'', 'KDH', 'ALI', 'HLAS-SD', 'REP'],
        'key': ['firm', 'date', 'sample',
                'OL\'aNO', 'SMER-SD', 'SR', 'L\'SNS', 'PS', 'SaS', 'ZL\'', 'KDH', 'ALI', 'HLAS-SD', 'REP',
                'Other', 'lead', 'end'],
        'col': {'OL\'aNO': (190, 214, 47), 'SMER-SD': (217, 39, 39), 'SR': (11, 76, 159), 'L\'SNS': (11, 87, 16),
                'PS': (0, 188, 255), 'SaS': (166, 206, 58), 'ZL\'': (255, 187, 0), 'KDH': (253, 209, 88),
                'ALI': (39, 93, 51), 'SNS': (37, 58, 121), 'DV': (255, 0, 43), 'HLAS-SD': (180, 40, 70),
                'REP': (220, 1, 22),
                'Government': (190, 214, 47), 'Opposition': (180, 40, 70),
                'Left': (180, 40, 70), 'Right': (190, 214, 47)},
        'gov': {'Government': ['OL\'aNO', 'SR', 'SaS', 'ZL\''],
                'Opposition': ['SMER-SD', 'L\'SNS', 'PS', 'KDH', 'ALI', 'HLAS-SD', 'REP']},
        'blocs': {'Left': ['SMER-SD', 'PS', 'HLAS-SD'],
                  'Right': ['OL\'aNO', 'SR', 'L\'SNS', 'SaS', 'ZL\'', 'KDH', 'ALI', 'REP']},
        'start': 0,
        'restart': ['http'],
        'end_date': Date(2024, 2, 24),
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Slovak_parliamentary_election&action=edit&section=3',
        'toggle_seats': True,
        'seats': 150,
        'divisor': 1,
        'bar': 0,
        'threshold': 5,
        'method': 'quotient'
    },
    'Slovenia': {
        'key': ['date', 'firm', 'publisher', 'sample',
                'SDS', 'LMS', 'SD', 'SMC', 'Left', 'NSi', 'SAB', 'DeSUS', 'SNS', 'SLS', 'PPS', 'DD', 'ACZS',
                'Other', 'None', 'Undecided', 'Abstain', 'lead', 'source', 'end'],
        'include': ['SDS', 'LMS', 'SD', 'SMC', 'Left', 'NSi', 'SAB', 'DeSUS', 'SNS', 'SLS', 'PPS', 'DD', 'ACZS'],
        'zeros': ['None', 'Undecided', 'Abstain'],
        'col': {'SDS': (252, 220, 0), 'LMS': (0, 90, 171), 'SD': (227, 0, 15), 'SMC': (0, 0, 153),
                'Left': (255, 55, 50), 'NSi': (0, 154, 199), 'SAB': (0, 169, 225), 'DeSUS': (141, 198, 63),
                'SNS': (34, 31, 31), 'SLS': (116, 202, 55), 'PPS': (210, 105, 30), 'DD': (129, 215, 66),
                'ACZS': (106, 179, 46)},
        'gov': {'Government': ['SDS', 'SMC', 'NSi'],
                'Opposition': ['LMS', 'SD', 'Left', 'SAB', 'DeSUS', 'SNS', 'SLS', 'PPS', 'DD', 'ACZS']},
        'blocs': {'Conservative': ['SDS', 'NSi', 'SNS', 'SLS'],
                  'Liberal': ['LMS', 'SMC', 'SAB', 'DeSUS', 'PPS', 'DD', 'ACZS'],
                  'Socialist': ['SD', 'Left']},
        'start': -22,
        'end_date': Date(2022, 6, 5),
        'restart': ['http'],
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Slovenian_parliamentary_election&action=edit&section=3',
        'toggle_seats': True,
        'seats': 88,
        'divisor': 1,
        'threshold': 4,
        'bar': 0,
        'method': 'quotient',
    },
    'Spain': {
        'include': ['PSOE', 'PP', 'VOX', 'UP', 'Cs', 'ERC', 'MP', 'JxCat', 'PNV', 'EHB', 'CUP', 'CC', 'BNG', 'NA+',
                    'PRC'],
        'key': ['firm', 'date', 'sample', 'turnout',
                'PSOE', 'PP', 'VOX', 'UP', 'Cs', 'ERC', 'MP', 'JxCat', 'PNV', 'EHB', 'CUP', 'CC', 'BNG', 'NA+',
                'PRC', 'lead', 'end'],
        'col': {'PSOE': (239, 28, 39), 'PP': (29, 132, 206), 'VOX': (99, 190, 33), 'UP': (123, 73, 119),
                'Cs': (235, 97, 9), 'ERC': (255, 178, 50), 'MP': (15, 222, 196), 'JxCat': (0, 199, 174),
                'PNV': (74, 174, 74), 'EHB': (181, 207, 24), 'CUP': (255, 237, 0), 'CC': (255, 215, 0),
                'BNG': (173, 207, 239), 'NA+': (129, 157, 163), 'PRC': (194, 206, 12),
                'Government': (239, 28, 39), 'Opposition': (29, 132, 206),
                'Left': (239, 28, 39), 'Right': (29, 132, 206), 'Regionalist': (255, 178, 50)},
        'gov': {'Government': ['PSOE', 'UP', 'PNV', 'MP', 'BNG'],
                'Opposition': ['PP', 'VOX', 'Cs', 'JxCat', 'CUP', 'CC', 'PRC']},
        'blocs': {'Left': ['PSOE', 'UP', 'MP'], 'Right': ['PP', 'VOX', 'Cs'],
                  'Regionalist': ['ERC', 'JxCat', 'PNV', 'EHB', 'CUP', 'CC', 'BNG', 'NA+', 'PRC']},
        'restart': ['http'],
        'start': 0,
        'end_date': Date(2023, 12, 10),
        'vlines': {Date(2021, 5, 4): 'Madrilenian election', Date(2021, 2, 14): 'Catalan election'},
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_Spanish_general_election&action=edit&section=4'
    },
    'Sweden': {
        'key': ['firm', 'date', 'sample',
                'V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD',
                'Other', 'lead', 'end'],
        'include': ['V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD'],
        'col': {'V': (176, 0, 0), 'S': (237, 27, 52), 'MP': (43, 145, 44), 'C': (1, 106, 57), 'L': (0, 106, 179),
                'M': (1, 156, 219), 'KD': (0, 70, 120), 'SD': (254, 223, 9),
                'Red-Green': (237, 27, 52), 'Alliance': (245, 137, 28),
                'Government': (237, 27, 52), 'Opposition': (245, 137, 28)},
        'blocs': {'Red-Green': ['S', 'V', 'MP'], 'Alliance': ['C', 'L', 'M', 'KD'], 'Right': ['M', 'L', 'KD', 'SD'],
                  'Left': ['C', 'S', 'V', 'MP']},
        'gov': {'Government': ['S', 'MP', 'V', 'C', 'L'], 'Opposition': ['M', 'KD', 'SD']},
        'start': 0,
        'restart': ['http'],
        'end_date': Date(2022, 9, 11),
        'toggle_seats': True,
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_2022_Swedish_general_election&action=edit&section=3',
        'seats': 349,
        'divisor': 2,
        'bar': 0.2,
        'threshold': 4,
        'method': 'quotient'
    },
    'UK': {
        'include': ['Conservative', 'Labour', 'Lib Dem', 'SNP', 'Green'],
        'key': ['date', 'firm', 'publisher', 'area', 'sample',
                'Conservative', 'Labour', 'Lib Dem', 'SNP', 'Green',
                'Other', 'lead', 'end'],
        'col': {'Conservative': (0, 135, 220), 'Labour': (228, 0, 59), 'Lib Dem': (250, 166, 26),
                'SNP': (253, 243, 142), 'Green': (106, 176, 35)},
        'start': -1,
        'vlines': {Date(2020, 4, 4): 'Starmer becomes Labour leader',
                   Date(2021, 5, 6): 'Local elections'},
        'end_date': Date(2024, 5, 2),
        'old_data': 'polling_data/old_uk_polling.txt',
        'url': 'https://en.wikipedia.org/w/index.php?title='
               'Opinion_polling_for_the_next_United_Kingdom_general_election&action=edit&section=3'
    }
}
