from base_ui import *
from toolkit import *
import date_kit
import types
import datetime
import urllib.request
import urllib.error
import threading
import csv
from bs4 import BeautifulSoup


def display_tables(tables, trunc=32):
    for d in tables:
        display_table(d['table'], d['key'], d['years'], trunc)


def display_table(table: List[List[Union[str, bool]]], key, years, trunc=32):
    for title in key:
        print(title.ljust(trunc, ' '), end='')
    print()
    for i, row in enumerate(table):
        if i in years:
            print(years[i])
        for col in row:
            txt = str(col)
            if len(txt) > trunc - 4:
                txt = txt[:trunc - 4]
            ntxt = ''
            for c in txt:
                if c != '\t':
                    ntxt += c
            print(ntxt.ljust(trunc, ' '), end='')
        print()


def transcribe_table(content, key, choice, begin, start):
    table: List[List[Any]] = []
    tables: List[Dict[str, Union[List[List[Any]], List[str]]]] = []
    years: Dict[int, str] = {0: str(today.year)}
    i = 0
    row = 0
    col = 0
    started = False
    s = ''
    for line in content:
        if len(line.strip()) > 0 and line.strip()[-1] == '|':
            ns = line.strip() + '~'
        else:
            ns = line.strip()
        if not ('{{' in line and '}}' not in line[line.find('{{'):]):
            ns += '|'
        if ns[0] == '!' and len(ns) > 1:
            ns = '|' + ns[1:]
        s += ns
    content = s.split('||')
    ncontent = []
    j = 0
    while j < len(content) - 1:
        line = content[j]
        for p in range(len(line) - 2):
            if line[p:p + 2] == '{{' and '}}' not in line[p + 2:]:
                line = line + '|' + content[j + 1]
                j += 1
                break
        ncontent.append(line)
        j += 1
    ncontent.append(content[-1])
    content = ncontent

    found = set()
    while i < len(content):
        line = content[i].strip('| \n')
        reset = False
        nkey = []
        if choice == 'Russia':
            if '===2021===' in line:
                nkey = ['date', 'firm',
                        'UR', 'CPRF', 'LDPR', 'SRZP', 'Other', 'Undecided', 'Abstention',
                        'lead', 'end']
                reset = True
        elif choice == 'Canada':
            if '===Campaign period===' in line:
                nkey = ['firm', 'date', 'link',
                        'LIB', 'CON', 'NDP', 'BQ', 'GRN', 'PPC',
                        'margin', 'size', 'method', 'lead', 'end']
                reset = True
        elif choice == 'Brazil':
            if 'Before August' in line:
                nkey = ['firm', 'date', 'sample',
                        'Bolsanaro (APB)', 'Lula (PT)', 'Haddad (PT)', 'Dino (PCdoB)', 'Gomes (PDT)', 'Boulos (PSOL)',
                        'Doria (PSDB)', 'Amoedo (NOVO)', 'Silva (REDE)', 'Moro', 'Huck',
                        'Other', 'Undecided', 'end']
                reset = True
        elif choice == 'Italy':
            a = 'https://www.youtrend.it/2021/05/25/draghi-cento-giorni/ Quorum – YouTrend'
            b = 'style="background:{{Power to the People (Italy)/meta/color}}'
            if a not in found and a in line:
                nkey = ['date', 'firm', 'sample',
                        'M5S', 'PD', 'Lega', 'FI', 'FdI', 'LeU', '+Eu', 'EV', 'C!', 'A', 'IV',
                        'Other', 'lead', 'end']
                reset = True
                found.add(a)
            elif b not in found and b in line:
                nkey = ['date', 'firm', 'sample',
                        'M5S', 'PD', 'Lega', 'FI', 'FdI', 'LeU', '+Eu', 'NcI', 'PaP',
                        'Other', 'lead', 'end']
                reset = True
                found.add(b)
        elif choice == 'Germany':
            if '=== 2020 ===' in line:
                nkey = ['firm', 'date', 'sample', 'abs',
                        'CDU/CSU', 'SPD', 'AfD', 'FDP', 'Linke', 'Gr\u00fcne',
                        'Other', 'lead', 'end']
                reset = True
        elif choice == 'Japan':
            if '=== 2020 ===' in line:
                nkey = ['date', 'firm',
                        'LDP', 'CDP', 'NKP', 'JCP', 'Ishin', 'DPP', 'SDP', 'Reiwa', 'Kibo', 'NHK',
                        'Other', 'None', 'lead', 'end']
                reset = True
        elif choice == 'Estonia':
            if '=== 2020 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'Reform', 'Centre', 'EKRE', 'Isamaa', 'SDE', 'E200', 'Green', 'TULE/EVA',
                        'Other', 'lead', 'gov', 'opp', 'end']
                reset = True
        elif choice == 'Poland':
            if '=== 2020 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'United Right', 'Civic Coalition', 'Civic Coalition', 'The Left', 'Polish Coalition',
                        'Kukiz\'15', 'Confederation', 'Poland 2050',
                        'Other', 'lead', 'end']
                reset = True
            elif '=== 2019 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Confederation',
                        'Other', 'lead', 'end']
                reset = True
            elif 'Dismissal of Deputy Prime Minister [[Jarosław Gowin]] and several deputy ministers' in line:
                nkey = ['firm', 'date', 'sample',
                        'United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Kukiz\'15', 'Confederation',
                        'Poland 2050',
                        'Other', 'lead', 'end']
                reset = True

        elif choice == 'Austria':
            if '=== By state ===' in line:
                break
        elif choice == 'Ireland':
            if '==National opinion polls==' in line:
                nkey = ['date', 'firm', 'sample',
                        'FG', 'FF', 'SF', 'Lab', 'PBP/S', 'SD', 'GP', 'O/I', 'O/I', 'O/I',
                        'end']
                reset = True
        elif choice == 'Netherlands':
            if '{{For|events during those years|2020 in the Netherlands|2019 in the Netherlands|' \
               '2018 in the Netherlands|2017 in the Netherlands}}' in line:
                nkey = ['firm', 'date',
                        'VVD', 'PVV', 'CDA', 'D66', 'GL', 'SP', 'PvdA', 'CU', 'PvdD', '50+', 'SGP', 'DENK', 'FVD',
                        'JA21', 'Volt', 'BIJ1', 'BBB',
                        'Others', 'lead', 'end']
                reset = True
        elif choice == 'Bulgaria':
            if 'https://bntnews.bg/news/parvi-prognozni-rezultati-6-partii-vlizat-v-parlamenta-stotni-' \
               'delyat-gerb-i-itn-1162099news.html' in line:
                nkey = ['firm', 'date', 'sample',
                        'GERB', 'ITN', 'BSPzB', 'DPS', 'DB', 'IBG-NI', 'BP', 'BP', 'BP', 'Revival', 'BL', 'RzB',
                        'LSChSR',
                        'Other', 'lead', 'end']
                reset = True

        if reset:
            tables.append({'table': table, 'key': key, 'years': years})
            table = []
            years = {0: years[max(years)]}
            row = 0
            col = 0
            key = nkey
        if '==' in line:
            yline = line[line.find('=='):]
            yline = yline[:yline.find('==', 3)].strip('= \n')
            try:
                int(yline)
            except ValueError:
                pass
            else:
                years[row] = yline
            i += 1
            col = 0
            started = False
            continue
        if not started:
            for b in begin:
                if b in line:
                    started = True
                    i += start
                    line = content[i].strip('| \n')
                    break
        if started:
            if len(line) > 0 and line[0] == '}':
                started = False
                i += 1
                col = 0
                continue
            elif len(line) > 0 and (col == 0 and line[0] == '-'):
                i += 1
                continue
            if len(table) <= row:
                placeholder = [True for _ in range(len(key))]
                table.extend([placeholder.copy() for _ in range(row - len(table) + 1)])
            while table[row][col] is False:
                col += 1
                if col >= len(key):
                    col -= len(key)
                    row += 1
                    if len(table) <= row:
                        placeholder = [True for _ in range(len(key))]
                        table.extend([placeholder.copy() for _ in range(row - len(table) + 1)])
            table[row][col] = line
            if 'colspan' in line and 'rowspan' in line:
                htemp: str = line[line.find('colspan') + len('colspan'):]
                hnum = int(htemp.strip('|= ').split()[0].split('|')[0].strip('" '))
                vtemp: str = line[line.find('rowspan') + len('rowspan'):]
                vnum = int(vtemp.strip('|= ').split()[0].split('|')[0].strip('" '))
                for r in range(vnum):
                    if len(table) <= row + vnum:
                        placeholder = [True for _ in range(len(key))]
                        table.extend([placeholder.copy() for _ in range(row + vnum - len(table) + 1)])
                    for c in range(hnum):
                        if col + c >= len(table[row]) - 1:
                            break
                        elif c + r != 0:
                            table[row + r][col + c] = False
            elif 'colspan' in line:
                temp: str = line[line.find('colspan') + len('colspan'):]
                num = int(temp.strip('|= ').split()[0].split('|')[0].strip('" '))
                for a in range(1, num):
                    if col + a >= len(table[row]) - 1:
                        break
                    else:
                        table[row][col + a] = False
            elif 'rowspan' in line:
                temp: str = line[line.find('rowspan') + len('rowspan'):]
                num = int(temp.strip('|= ').split()[0].split('|')[0].strip('" '))
                if len(table) <= row + num:
                    placeholder = [True for _ in range(len(key))]
                    table.extend([placeholder.copy() for _ in range(row + num - len(table) + 1)])
                for a in range(1, num):
                    table[row + a][col] = False
            col += 1
            if col >= len(key):
                col -= len(key)
                row += 1
        i += 1
    tables.append({'table': table, 'key': key, 'years': years})
    return tables


def process_tables(tables: List[Dict[str, Union[List[List[Any]], List[str]]]], choice, include, zeros):
    for i, table in enumerate(tables):
        tables[i] = {'table': process_table(table['table'], table['years'], table['key'], choice, include, zeros),
                     'years': table['years'],
                     'key': table['key']}
    return tables


def process_table(table: List[List[Any]], years, key, choice, include, zeros):
    def process_date(line, year) -> Optional[int]:
        line = line.strip().strip('}\'')
        if choice == 'UK' and 'opdrts' in line:
            temp = line.strip('|').split('|')
            if temp[-1] == 'year':
                shift = True
            else:
                shift = False
            y = temp[-1 - shift]
            m = temp[-2 - shift]
            d = temp[-3 - shift]
            temp = d + ' ' + m + ' ' + y
        elif choice == 'Ireland' and 'dts' in line:
            temp = line.strip('|').split('|')
            y = temp[-1]
            m = temp[-2]
            d = temp[-3]
            temp = y + ' ' + m + ' ' + d
        else:
            if '{{efn' in line:
                line = line[:line.find('{{efn')]
            dates = line.split('|')[-1]
            if '-' in dates:
                s = dates.split('-')
            elif '–' in dates:
                s = dates.split('–')
            elif '−' in dates:
                s = dates.split('−')
            else:
                s = dates.split('â€“')
            temp = s[-1].strip().strip('\'}')
            if choice == 'Israel':
                temps = temp.split()
                if len(temps[-1]) < 3:
                    temps[-1] = '20' + temps[-1]
                temp = ''
                for s in temps:
                    temp += s + ' '
        temps = temp.strip().split()
        if len(temps) == 2:
            try:
                y = int(temps[-1])
                m = temps[0]
                temp = str(date_kit.get_month_length(date_kit.get_month_number(m), y)) + ' ' + temp
            except ValueError:
                temp = temp + ' ' + year
        elif len(temps) == 1:
            try:
                temp = str(date_kit.get_month_length(date_kit.get_month_number(temps[0]), year)) + \
                       ' ' + temp + ' ' + year
            except KeyError:
                return None
        temp = temp.replace('X', '0')
        try:
            if choice in ['Canada', 'Ontario']:
                form = 'mdy'
            else:
                form = 'dmy'
            end_date = date_kit.Date(text=temp, form=form)
        except ValueError:
            return None
        end = date_kit.date_dif(today, end_date)
        return end

    def process_value(s, choice):
        temp = s
        if 'style="color:#F8F9FA;"' in temp:
            return None
        if '{{efn' in temp:
            temp = temp[:temp.find('{{efn')]
        if '<br' in temp:
            temp = temp[:temp.find('<br')]
        if '<ref' in temp:
            temp = temp[:temp.find('<ref')]
        if choice == 'Israel':
            if '<!--' in temp:
                temp = temp[:temp.find('<!--')]
        elif choice == 'Japan':
            temp = temp.split(' ')[-1]
        temp = temp.split('|')[-1].strip()
        temp = temp.replace(',', '.')
        if temp in ['â€“', '-', '', '–'] or "small" in temp:
            if choice == 'Israel':
                share = 0
            else:
                share = None
        else:
            try:
                share = float(temp.strip().strip("'%!\""))
                if choice == 'Netherlands':
                    share *= 2 / 3
                elif choice == 'Israel':
                    share *= 5 / 6
            except ValueError:
                share = None
        return share

    date_i: int = key.index('date')
    if zeros is None:
        zeros = []
    indices: List[int] = []
    for i, k in enumerate(key):
        if k in include + zeros + ['Other']:
            indices.append(i)
    remove = []
    year = None
    for i in range(len(table)):
        if i in years:
            year = years[i]
        entry = table[i]
        date = entry[date_i]
        if type(date).__name__ != 'str':
            if date is False:
                for j in range(i - 1, -1, -1):
                    t = table[j][date_i]
                    if type(t).__name__ == 'int':
                        date = t
                        break
            else:
                remove.append(i)
                continue
        else:
            date = process_date(entry[date_i], year)
        if date is None:
            remove.append(i)
        else:
            table[i][date_i] = date

        for j in indices:
            if type(entry[j]).__name__ == 'str':
                val = process_value(entry[j], choice)
            elif entry[j] is False:
                val = None
            else:
                val = entry[j]
            table[i][j] = val

    for r in sorted(remove, reverse=True):
        table.pop(r)
    return table


def filter_tables(tables: List[Dict[str, Union[List[List[Any]], List[str]]]], choice, include):
    for i, table in enumerate(tables):
        tables[i] = {'table': filter_table(table['table'], table['key'], choice, include),
                     'key': table['key'],
                     'years': table['years']}
    return tables


def filter_table(table: List[List[Any]], key: List[str], choice, include):
    purge = set()
    for r, entry in enumerate(table):
        count = 0
        for i, k in enumerate(key):
            if k in include and entry[i] is not None:
                count += 1
                if count > 1:
                    break
        else:
            purge.add(r)
    if choice == 'Czechia':
        for p in ['SPOLU', 'Pirati+STAN']:
            c = key.count(p)
            if c > 1:
                i = key.index(p)
                for j in range(1, c):
                    for k, entry in enumerate(table):
                        if entry[i + j] is not None:
                            purge.add(k)
    elif choice == 'Brazil':
        i = key.index('firm')
        for k, entry in enumerate(table):
            if type(entry[i]).__name__ == 'str':
                if '2018 Brazilian general election' in entry[i]:
                    purge.add(k)
    elif choice == 'Hungary':
        i = key.index('firm')
        for k, entry in enumerate(table):
            if type(entry[i]).__name__ == 'str':
                if '2019 Hungarian local elections' in entry[i]:
                    purge.add(k)
    elif choice == 'Slovenia':
        i = key.index('Other')
        for k, entry in enumerate(table):
            for fig in entry[i:i + 4]:
                if fig is not None:
                    break
            else:
                purge.add(k)
    elif choice == 'Poland':
        i = key.index('firm')
        for k, entry in enumerate(table):
            if type(entry[i]).__name__ == 'str':
                if 'Presidential election' in entry[i]:
                    purge.add(k)
    for j, entry in enumerate(table):
        for i, k in enumerate(key):
            if k in include and entry[i] is not False:
                break
        else:
            purge.add(j)
    for k in sorted(purge, reverse=True):
        table.pop(k)
    return table


def modify_tables(tables: List[Dict[str, Union[List[List[Any]], List[str]]]], choice, include, zeros):
    for i, table in enumerate(tables):
        tables[i] = {'table': modify_table(table['table'], table['key'], choice, include, zeros),
                     'key': table['key'],
                     'years': table['years']}
    return tables


def modify_table(table: List[List[Any]], key: List[str], choice, include, zeros):
    if zeros is None:
        return table
    else:
        for j, entry in enumerate(table):
            normalize = 0
            for i, e in enumerate(entry):
                if key[i] in zeros:
                    if choice == 'Russia' and normalize == 0 and e is False:
                        a = entry[i - 1]
                    elif e is None:
                        a = 0
                    else:
                        a = e
                    normalize += a
            q = 1 - normalize / 100
            for i, e in enumerate(entry):
                if key[i] in include:
                    if e is None:
                        continue
                    else:
                        table[j][i] = e / q
        return table


def interpret_tables(tables: List[Dict[str, Union[List[List[Any]], List[str]]]], include):
    all_dat: Dict[str, Dict[int, List[float]]] = {}
    for table in tables:
        dat = interpret_table(table['table'], table['key'], include)
        for p in dat:
            if p not in all_dat:
                all_dat[p] = {}
            for x, ys in dat[p].items():
                if x not in all_dat[p]:
                    all_dat[p][x] = []
                all_dat[p][x].extend(ys)
    return all_dat


def interpret_table(table: List[List[Any]], key: List[str], include):
    dat: Dict[str, Dict[int, List[float]]] = {}
    indices: List[int] = []
    date_i = key.index('date')
    for i, k in enumerate(key):
        if k in include:
            indices.append(i)
    for i in indices:
        p = key[i]
        if p in dat:
            continue
        else:
            dat[p] = {}
            c = key.count(p)
            for entry in table:
                date = entry[date_i]
                tot = entry[i]
                if c > 1:
                    for j in range(1, c):
                        if tot is None:
                            tot = entry[i + j]
                        elif entry[i + j] is not None:
                            tot += entry[i + j]
                if date in dat[p]:
                    dat[p][date].append(tot)
                else:
                    dat[p][date] = [tot]
    return dat


def choices_setup():
    choices = {
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
            'key': ['firm', 'date', 'sample', 'Bolsanaro (APB)', 'Lula (PT)', 'Gomes (PDT)', 'Doria (PSDB)',
                    'Leite (PSDB)', 'Mandetta (DEM)', 'Pancheco (DEM)', 'Datena (PSL)', 'Moro', 'Other', 'Undecided',
                    'end'],
            'include': ['Bolsanaro (APB)', 'Lula (PT)', 'Gomes (PDT)', 'Doria (PSDB)'],
            'zeros': ['Undecided'],
            'col': {'Bolsanaro (APB)': (0, 140, 0), 'Lula (PT)': (204, 0, 0), 'Haddad (PT)': (204, 0, 0),
                    'Dino (PCdoB)': (163, 0, 0), 'Gomes (PDT)': (238, 100, 100), 'Boulos (PSOL)': (163, 0, 0),
                    'Doria (PSDB)': (0, 95, 164), 'Amoedo (NOVO)': (240, 118, 42), 'Silva (REDE)': (46, 139, 87),
                    'Moro': dark_grey, 'Huck': grey},
            'start': 0,
            'vlines': {Date(2021, 3, 8): "Lula cleared of charges"},
            'end_date': Date(2022, 10, 2),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_2022_Brazilian_general_election&action=edit&section=3',
        },
        'Bulgaria': {
            'include': ['ITN', 'GERB', 'BSPzB', 'DB', 'DPS', 'IBG-NI', 'BP', 'Revival'],
            'key': ['firm', 'date', 'sample',
                    'ITN', 'GERB', 'BSPzB', 'DB', 'DPS', 'IBG-NI', 'BP', 'Revival',
                    'Other', 'lead', 'end'],
            'col': {'GERB': (0, 86, 167), 'ITN': (75, 185, 222), 'BSPzB': (219, 15, 40), 'DPS': (0, 96, 170),
                    'DB': (0, 74, 128), 'IBG-NI': (91, 165, 70), 'BP': black, 'Revival': (192, 159, 98),
                    'BL': (243, 129, 20), 'RzB': (43, 74, 153), 'LSChSR': (241, 25, 40)},
            'blocs': {'Conservative': ['GERB'], 'Socialist': ['BSPzB'], 'Liberal': ['DPS'],
                      'Nationalist': ['BP', 'Revival'],
                      'Populist': ['ITN', 'DB', 'IBG-NI']},
            'start': 0,
            'end_date': Date(2025, 9, 30),
            'toggle_seats': True,
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Next_Bulgarian_parliamentary_election&action=edit&section=3',
            'old_data': 'polling_data/old_bulgaria_polling.txt',
            'seats': 240,
            'method': 'remainder',
            'threshold': 4
        },
        'Canada': {
            'key': ['firm', 'date', 'link',
                    'CON', 'LIB', 'NDP', 'BQ', 'GRN', 'PPC',
                    'Other', 'margin', 'size', 'method', 'lead', 'end'],
            'include': ['CON', 'LIB', 'NDP', 'BQ', 'GRN', 'PPC'],
            'col': {'CON': (100, 149, 237), 'LIB': (234, 109, 106), 'NDP': (244, 164, 96), 'BQ': (135, 206, 250),
                    'GRN': (153, 201, 85), 'PPC': (131, 120, 158),
                    'Government': (234, 109, 106), 'Opposition': (100, 149, 237)},
            'gov': {'Government': ['LIB'], 'Opposition': ['CON', 'NDP', 'BQ', 'GRN', 'PPC']},
            'blocs': {'Progressive': ['LIB', 'NDP', 'BQ', 'GRN'], 'Conservative': ['CON', 'PPC']},
            'start': 0,
            'restart': ['Innovative Research', '2019 election'],
            'vlines': {Date(2019, 10, 21): "General Election",
                       Date(2020, 8, 24): "O'Toole elected Conservative leader",
                       Date(2017, 10, 1): "Singh elected NDP leader",
                       Date(2017, 5, 27): "Scheer elected Conservative leader"},
            'end_date': Date(2023, 10, 16),
            'toggle_seats': True,
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_44th_Canadian_federal_election&action=edit&section=1',
            'old_data': 'polling_data/old_canada_polling.txt'
        },
        'Czechia': {
            'key': ['firm', 'date', 'size', 'turnout',
                    'ANO', 'SPOLU', 'SPOLU', 'SPOLU', 'Pirati+STAN', 'Pirati+STAN', 'SPD', 'KSCM', 'CSSD', 'T-S',
                    'T-S', 'Z', 'ODA', 'P',
                    'Other', 'Lead', 'Govt.', 'Opp.', 'end'],
            'include': ['ANO', 'SPOLU', 'SPOLU', 'SPOLU', 'Pirati+STAN', 'Pirati+STAN', 'SPD', 'KSCM', 'CSSD', 'T-S',
                        'T-S', 'Z', 'ODA', 'P'],
            'col': {'ANO': (38, 16, 96), 'SPOLU': (35, 44, 119), 'Pirati+STAN': (0, 0, 0), 'SPD': (33, 117, 187),
                    'KSCM': (204, 0, 0), 'CSSD': (236, 88, 0), 'T-S': (0, 150, 130), 'Z': (96, 180, 76),
                    'P': (0, 51, 255), 'ODA': (0, 45, 114),
                    'Government': (38, 16, 96), 'Opposition': (0, 0, 0)},
            'gov': {'Government': ['ANO', 'KSCM', 'CSSD'],
                    'Opposition': ['SPOLU', 'Pirati+STAN', 'SPD', 'T-S', 'Z', 'P']},
            'end_date': Date(2021, 10, 9),
            'start': 0,
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_2021_Czech_legislative_election&action=edit&section=3',
            'toggle_seats': True,
            'seats': 200,
            'divisor': 1,
            'bar': 0,
            'threshold': 5,
            'method': 'quotient'
        },
        'Denmark': {
            'key': ['firm', 'date', 'sample',
                    'A', 'V', 'O', 'B', 'F', '\u00d8', 'C', '\u00c5', 'D', 'I', 'P', 'K', 'E', 'G',
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
            'include': ['CDU/CSU', 'SPD', 'AfD', 'FDP', 'Linke', 'Gr\u00fcne'],
            'key': ['firm', 'date', 'sample', 'abs',
                    'CDU/CSU', 'SPD', 'AfD', 'FDP', 'Linke', 'Gr\u00fcne',
                    'FW', 'Other', 'lead', 'end'],
            'col': {'CDU/CSU': (0, 0, 0), 'Gr\u00fcne': (100, 161, 45), 'SPD': (235, 0, 31), 'FDP': (255, 237, 0),
                    'AfD': (0, 158, 224), 'Linke': (190, 48, 117),
                    'Red-Red-Green': (190, 48, 117), 'Black-Yellow': (255, 237, 0), 'Jamaica': (118, 132, 15),
                    'Grand Coalition': (0, 0, 0), 'Traffic Light': (235, 0, 31), 'Black-Green': (100, 161, 45),
                    'Old Guard': (245, 118, 15)},
            'blocs': {'Red-Red-Green': ['Gr\u00fcne', 'SPD', 'Linke'],
                      'Black-Yellow': ['CDU/CSU', 'FDP'],
                      'Jamaica': ['CDU/CSU', 'FDP', 'Gr\u00fcne'],
                      'Traffic Light': ['SPD', 'Gr\u00fcne', 'FDP'],
                      'Grand Coalition': ['CDU/CSU', 'SPD'],
                      'Black-Green': ['CDU/CSU', 'Gr\u00fcne'],
                      'Old Guard': ['CDU/CSU', 'SPD', 'FDP']},
            'gov': {'Government': ['CDU/CSU', 'SPD'], 'Opposition': ['Gr\u00fcne', 'Linke', 'FDP', 'AfD']},
            'start': 0,
            'end_date': Date(2021, 9, 26),
            'toggle_seats': True,
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_2021_German_federal_election&action=edit&section=3',
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
            'blocs': {'Socialist': ['V', 'S', 'J'], 'Liberal': ['B', 'M', 'C', 'P'], 'Conservative': ['D', 'F']},
            'gov': {'Government': ['V', 'B', 'D'], 'Opposition': ['S', 'M', 'P', 'F', 'C', 'J']},
            'start': 0,
            'end_date': Date(2021, 9, 25),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_next_Icelandic_parliamentary_election&action=edit&section=2',
            'toggle_seats': True,
            'divisor': 1,
            'bar': 0,
            'method': 'quotient',
            'threshold': 5,
            'seats': 63
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
            'restart': ['Cite web', 'cite web', 'General election', 'cite news', 'Cite news'],
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
            'gov': {'Government': ['LDP'],
                    'Opposition': ['CDP', 'NKP', 'JCP', 'Ishin', 'DPP', 'SDP', 'Reiwa', 'NHK']},
            'zeros': ['None'],
            'col': {'LDP': (60, 163, 36), 'CDP': (24, 69, 137), 'NKP': (245, 88, 129), 'JCP': (219, 0, 28),
                    'Ishin': (184, 206, 67), 'DPP': (255, 215, 0), 'SDP': (28, 169, 233), 'Reiwa': (237, 0, 140),
                    'NHK': (248, 234, 13)},
            'start': -1,
            'end_date': Date(2021, 10, 22),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_2021_Japanese_general_election&action=edit&section=9',
            'old_data': 'polling_data/old_japan_polling.txt'
        },
        'Latvia': {
            'key': ['date', 'firm', 'sample',
                    'SDPS', 'PCL', 'JKP', 'AP!', 'NA', 'ZZS', 'JV', 'LRA', 'LKS', 'PRO', 'LuK', 'Other', 'Undecided',
                    'None', 'lead', 'end'],
            'include': ['SDPS', 'PCL', 'JKP', 'AP!', 'NA', 'ZZS', 'JV', 'LRA', 'LKS', 'PRO', 'LuK'],
            'col': {'SDPS': (238, 34, 43), 'PCL': (0, 172, 180), 'JKP': (24, 41, 86), 'AP!': (255, 221, 0),
                    'NA': (147, 35, 48), 'ZZS': (2, 114, 58), 'JV': (106, 182, 71), 'LRA': (14, 50, 103),
                    'LKS': (53, 96, 169), 'PRO': (230, 70, 50), 'LuK': (36, 28, 36)},
            'gov': {'Government': ['JKP', 'AP!', 'NA', 'JV'],
                    'Opposition': ['SDPS', 'ZZS', 'PCL', 'LuK', 'PRO', 'LRA', 'LKS']},
            'blocs': {'Conservative': ['JKP', 'NA', 'PCL', 'ZZS', 'JV', 'LuK'],
                      'Socialist': ['SDPS', 'PRO', 'LKS'],
                      'Liberal': ['LRA', 'AP!']},
            'zeros': ['Undecided', 'None'],
            'start': -1,
            'end_date': Date(2022, 9, 1),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   '2022_Latvian_parliamentary_election&action=edit&section=2',
            'toggle_seats': True,
            'seats': 100,
            'divisor': 2,
            'method': 'quotient',
            'threshold': 5,
            'bar': 0,
        },
        'Lithuania': {
            'include': ['TS-LKD', 'LVZS', 'DP', 'LSDP', 'Laisves', 'LRLS', 'LLRA', 'LSDDP', 'LCP', 'LT'],
            'key': ['firm', 'date',
                    'TS-LKD', 'LVZS', 'DP', 'LSDP', 'Laisves', 'LRLS', 'LLRA', 'LSDDP', 'LCP', 'LT',
                    'lead', 'end'],
            'col': {'TS-LKD': (0, 165, 155), 'LVZS': (0, 144, 53), 'DP': (29, 87, 140), 'LSDP': (225, 5, 20),
                    'Laisves': (227, 0, 107), 'LRLS': (244, 129, 0), 'LLRA': (120, 19, 35), 'LSDDP': (193, 39, 45),
                    'LCP': (0, 156, 61), 'LT': (251, 186, 0)},
            'gov': {'Government': ['TS-LKD', 'Laisves', 'LRLS'],
                    'Opposition': ['LVZS', 'DP', 'LSDP', 'LLRA', 'LSDDP', 'LCP', 'LT']},
            'blocs': {'Conservative': ['TS-LKD', 'LVZS', 'LCP', 'LLRA'], 'Liberal': ['LRLS', 'DP', 'Laisves', 'LT'],
                      'Socialist': ['LSDP', 'LSDDP']},
            'start': 0,
            'end_date': Date(2024, 10, 6),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   '2024_Lithuanian_parliamentary_election&action=edit&section=3'
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
            'restart': ['[http', '2017 election', '2021 election'],
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
            'blocs': {'Red-Green': ['R', 'SV', 'Ap', 'Sp'], 'Blue': ['V', 'KrF', 'H', 'FrP'], 'Green': ['MDG']},
            'start': 0,
            'end_date': Date(2021, 9, 13),
            'toggle_seats': True,
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_2021_Norwegian_parliamentary_election&action=edit&section=3',
            'seats': 169,
            'divisor': 2,
            'bar': 0.4,
            'threshold': 4,
            'method': 'quotient',
            'old_data': 'polling_data/old_norway_polling.txt'
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
                    'Confederation', 'Poland 2050',
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
            'end_date': Date(2023, 10, 8),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_next_Portuguese_legislative_election&action=edit&section=3',
            'toggle_seats': True,
            'seats': 200,
            'divisor': 1,
            'bar': 0,
            'threshold': 0,
            'method': 'quotient'
        },
        'Russia': {
            'key': ['date', 'firm',
                    'UR', 'CPRF', 'LDPR', 'SRZP',
                    'CR', 'Yabloko', 'RRPSJ', 'Rodina', 'PG', 'Greens', 'CP', 'RPFJ', 'NP', 'GA',
                    'Undecided', 'Abstention',
                    'lead', 'end'],
            'col': {'UR': (46, 78, 164), 'CPRF': (204, 17, 17), 'LDPR': (68, 136, 204), 'SRZP': (255, 192, 3),
                    'Yabloko': (0, 162, 61), 'RPPSJ': (197, 32, 48)},
            'include': ['UR', 'CPRF', 'LDPR', 'SRZP'],
            'zeros': ['Undecided', 'Abstention'],
            'start': -1,
            'end_date': Date(2021, 9, 19),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_2021_Russian_legislative_election&action=edit&section=4',
            'old_data': 'polling_data/old_russia_polling.txt',
            'vlines': {Date(2018, 6, 14): 'Retirement Age Increase Announced'},
        },
        'Slovakia': {
            'include': ['OL\'aNO', 'SMER-SD', 'SR', 'L\'SNS', 'PS-SPOLU', 'PS-SPOLU', 'SaS', 'ZL\'', 'KDH',
                        'Magyar', 'Magyar', 'Magyar', 'Magyar', 'SNS', 'DV', 'HLAS-SD', 'REP'],
            'key': ['date', 'firm', 'sample',
                    'OL\'aNO', 'SMER-SD', 'SR', 'L\'SNS', 'PS-SPOLU', 'PS-SPOLU', 'SaS', 'ZL\'', 'KDH',
                    'Magyar', 'Magyar', 'Magyar', 'Magyar', 'SNS', 'DV', 'HLAS-SD', 'REP',
                    'lead', 'end'],
            'col': {'OL\'aNO': (190, 214, 47), 'SMER-SD': (217, 39, 39), 'SR': (11, 76, 159), 'L\'SNS': (11, 87, 16),
                    'PS-SPOLU': (0, 188, 255), 'SaS': (166, 206, 58), 'ZL\'': (255, 187, 0), 'KDH': (253, 209, 88),
                    'Magyar': (39, 93, 51), 'SNS': (37, 58, 121), 'DV': (255, 0, 43), 'HLAS-SD': (180, 40, 70),
                    'REP': (220, 1, 22),
                    'Government': (190, 214, 47), 'Opposition': (180, 40, 70),
                    'Left': (180, 40, 70), 'Right': (190, 214, 47)},
            'gov': {'Government': ['OL\'aNO', 'SR', 'SaS', 'ZL\''],
                    'Opposition': ['SMER-SD', 'L\'SNS', 'PS-SPOLU', 'KDH', 'Magyar', 'SNS', 'DV', 'HLAS-SD', 'REP']},
            'blocs': {'Left': ['SMER-SD', 'PS-SPOLU', 'DV', 'HLAS-SD'],
                      'Right': ['OL\'aNO', 'SR', 'L\'SNS', 'SaS', 'ZL\'', 'KDH', 'Magyar', 'SNS', 'REP']},
            'start': -1,
            'restart': ['Focus', 'AKO', '2020 elections'],
            'end_date': Date(2024, 2, 24),
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_next_Slovak_parliamentary_election&action=edit&section=1',
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
            'restart': ['http', '2018 election'],
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
            'restart': ['[http', '2019 general election'],
            'end_date': Date(2024, 5, 2),
            'old_data': 'polling_data/old_uk_polling.txt',
            'url': 'https://en.wikipedia.org/w/index.php?title='
                   'Opinion_polling_for_the_next_United_Kingdom_general_election&action=edit&section=3'
        }
    }
    for c, d in choices.items():
        if 'restart' not in d:
            d['restart'] = ['[http']
        if 'date' not in d:
            d['date'] = 1
        if 'end_date' not in d:
            d['end_date'] = None
        if 'blocs' not in d:
            d['blocs'] = None
        elif d['blocs'] is not None:
            for line in d['blocs'].keys():
                if line not in d['col'].keys():
                    d['col'][line] = d['col'][d['blocs'][line][0]]
        if 'gov' not in d:
            d['gov'] = None
        elif d['gov'] is not None:
            for line in d['gov'].keys():
                if line not in d['col'].keys():
                    d['col'][line] = d['col'][d['gov'][line][0]]
        if 'file_name' not in d:
            d['file_name'] = 'polling_data/' + c.lower() + '_polling.txt'
        if 'include' not in d:
            d['include'] = None
        if 'vlines' not in d:
            d['vlines'] = None
        elif d['vlines'] is not None:
            vlines: Dict[Date, str] = d['vlines']
            d['vlines'] = {date_kit.date_dif(today, k): v for k, v in vlines.items()}
        if 'zeros' not in d:
            d['zeros'] = None
        if 'toggle_seats' not in d:
            d['toggle_seats'] = False
    return choices


def choice_setting(c):
    dat = choices[c]
    file_name = dat['file_name']
    key = dat['key']
    col = dat.get('col', None)
    blocs = dat['blocs']
    gov = dat['gov']
    start = dat.get('start', None)
    restart = dat['restart']
    date = dat['date']
    end_date = dat['end_date']
    include = dat['include']
    vlines = dat['vlines']
    toggle_seats = dat['toggle_seats']
    zeros = dat['zeros']
    return file_name, key, col, blocs, gov, start, restart, date, end_date, include, vlines, toggle_seats, zeros


def filter_nils(dat):
    return filter_trails(filter_nones(dat))


def filter_nones(dat):
    if dat is not None:
        for line, vals in dat.items():
            for x, ys in vals.items():
                dat[line][x] = list(filter(lambda y: y is not None, ys))
    return dat


def filter_trails(dat):
    if dat is not None:
        purge = {}
        for line, vals in dat.items():
            for x, ys in vals.items():
                for y in dat[line][x]:
                    if y is not None:
                        break
                else:
                    if line not in purge:
                        purge[line] = []
                    purge[line].append(x)
        for line in purge:
            for x in purge[line]:
                dat[line].pop(x)
    return dat


class GraphPage:
    spread = 60
    high_res = 3
    low_res = 21

    def __init__(self, choice, view='parties', metric='percentage', to_end_date=False):
        widgets.clear()

        self.graph = None
        self.choice = choice
        self.view = view
        self.metric = metric
        self.minx = -1
        self.spread = GraphPage.spread
        self.file_name, self.key, self.col, self.blocs, self.gov, self.start, self.restart, self.date, \
            self.end_date, self.include, self.vlines, toggle_seats, self.zeros \
            = choice_setting(self.choice)

        self.to_end_date = to_end_date

        self.dat = None
        self.party_dat = None
        self.blocs_dat = None
        self.gov_dat = None
        self.seats_party_dat = None
        self.seats_blocs_dat = None
        self.seats_gov_dat = None

        self.graph_dat = None
        self.graph_blocs_dat = None
        self.graph_gov_dat = None
        self.seats_graph_dat = None
        self.seats_graph_blocs_dat = None
        self.seats_graph_gov_dat = None

        height = screen_height / 12
        unit_size = height * 2 / 3
        back_button = Button((3 / 2 * unit_size, height * 2 / 3), (unit_size, unit_size), align=CENTER)
        back_button.callback(menu_page.show)
        img = Image(back_button.rect.center,
                    (back_button.rect.width * 3 / 4, back_button.rect.height * 3 / 4),
                    "images/arrow.png")
        img.surface = pygame.transform.rotate(img.surface, 270)
        back_button.set_tooltip("Return to Menu")
        back_button.components.append(img)
        back_button.show()

        pinboard = types.SimpleNamespace()
        pinboard.select_buttons = []

        bloc_button = SelectButton((screen_width - 3 / 2 * unit_size, height * 2 / 3),
                                   (unit_size, unit_size),
                                   align=CENTER, parent=pinboard, deselectable=False)
        pinboard.select_buttons.append(bloc_button)
        bloc_img = Image(bloc_button.rect.center, (bloc_button.rect.w * 4 / 5, bloc_button.rect.h * 4 / 5),
                         img_path='images/hierarchy.png')
        bloc_button.components.append(bloc_img)
        bloc_button.set_tooltip('Blocs')
        bloc_button.callback(functools.partial(self.change_view, 'blocs'))
        if self.blocs is None:
            bloc_button.disable()
        bloc_button.show()

        gov_button = SelectButton((screen_width - 3 * unit_size, height * 2 / 3),
                                  (unit_size, unit_size),
                                  align=CENTER, parent=pinboard, deselectable=False)
        gov_img = Image(gov_button.rect.center, (gov_button.rect.w * 4 / 5, gov_button.rect.h * 4 / 5),
                        img_path='images/parliament.png')
        gov_button.components.append(gov_img)
        gov_button.set_tooltip('Government/Opposition')
        pinboard.select_buttons.append(gov_button)
        gov_button.callback(functools.partial(self.change_view, 'gov'))
        if self.gov is None:
            gov_button.disable()
        gov_button.show()

        party_button = SelectButton((screen_width - 9 / 2 * unit_size, height * 2 / 3),
                                    (unit_size, unit_size),
                                    align=CENTER, parent=pinboard, deselectable=False)
        pinboard.select_buttons.append(party_button)
        party_img = Image(party_button.rect.center, (party_button.rect.w * 4 / 5, party_button.rect.h * 4 / 5),
                          img_path='images/ballot.png')
        party_button.components.append(party_img)
        party_button.set_tooltip('Parties')
        party_button.callback(functools.partial(self.change_view, 'parties'))
        party_button.select()
        party_button.show()

        seats_button = SelectButton((screen_width - 12 / 2 * unit_size, height * 2 / 3),
                                    (unit_size, unit_size), align=CENTER, deselectable=True)
        seats_button.callback(functools.partial(self.change_metric, 'seats'))
        seats_button.release_callback(functools.partial(self.change_metric, 'percentage'))
        seats_button.set_tooltip('Toggle estimated seat/vote distribution')
        seats_img = Image(seats_button.rect.center, (seats_button.rect.w * 4 / 5, seats_button.rect.h * 4 / 5),
                          img_path='images/cabinet.png')
        seats_button.components.append(seats_img)
        if not toggle_seats:
            seats_button.disable()
        seats_button.show()

        end_button = SelectButton((screen_width - 15 / 2 * unit_size, height * 2 / 3),
                                  (unit_size, unit_size), align=CENTER, deselectable=True)
        end_button.callback(functools.partial(self.change_toend, True))
        end_button.release_callback(functools.partial(self.change_toend, False))
        end_button.set_tooltip('Show up to next election')
        end_img = Image(end_button.rect.center, (end_button.rect.w * 4 / 5, end_button.rect.h * 4 / 5),
                        img_path='images/next.png')
        end_button.components.append(end_img)
        if self.end_date is None:
            end_button.disable()
        else:
            end_button.select()
        end_button.show()

        self.spread_txt = Text(str(self.spread), (back_button.rect.centerx, back_button.rect.bottom + 8), align=TOP)
        self.spread_txt.show()

        area = (self.spread_txt.rect.h, self.spread_txt.rect.h)
        self.up_spread = Button((self.spread_txt.rect.right + area[0] / 2, self.spread_txt.rect.centery), area,
                                align=LEFT)
        self.up_spread.callback(self.change_spread, returns=True)
        img = Image(self.up_spread.rect.center,
                    (self.up_spread.rect.width * 3 / 4, self.up_spread.rect.height * 3 / 4),
                    "images/arrow.png")
        img.surface = pygame.transform.rotate(img.surface, 90)
        self.up_spread.components.append(img)
        self.up_spread.show()

        self.down_spread = Button((self.spread_txt.rect.left - area[0] / 2, self.spread_txt.rect.centery), area,
                                  align=RIGHT)
        self.down_spread.callback(self.change_spread, returns=True)
        img = Image(self.down_spread.rect.center,
                    (self.down_spread.rect.width * 3 / 4, self.down_spread.rect.height * 3 / 4),
                    "images/arrow.png")
        img.surface = pygame.transform.rotate(img.surface, 270)
        self.down_spread.components.append(img)
        self.down_spread.show()

        pinboard2 = types.SimpleNamespace()
        pinboard2.select_buttons = []
        timescales = [1, 2, 5, 10, -1]
        for i, s in enumerate(timescales):
            b = SelectButton((screen_rect.centerx - (i - 2) * unit_size, height * 2 / 3),
                             (unit_size * 2 / 3, unit_size * 2 / 3), label='MAX' if s == -1 else str(s),
                             align=CENTER, parent=pinboard2, deselectable=False, exclusive=True,
                             label_size=int(BASE_FONT_SIZE * 3 / 4) if s == -1 else BASE_FONT_SIZE)
            b.callback(functools.partial(self.change_minx, s))
            if s == -1:
                b.select()
            b.show()
            pinboard2.select_buttons.append(b)

        self.change_view(view='parties')

        remove_from_update(self.choice)

        close_button()

    def init_dat(self):
        with open(self.file_name, 'r', encoding='utf-8') as f:
            content = f.readlines()
        if 'old_data' in choices[self.choice]:
            with open(choices[self.choice]['old_data'], 'r', encoding='utf-8') as f:
                content.extend(f.readlines())
        tables = transcribe_table(content, self.key, self.choice, self.restart, self.start)
        display_tables(tables)
        tables = process_tables(tables, self.choice, self.include, self.zeros)
        tables = filter_tables(tables, self.choice, self.include)
        tables = modify_tables(tables, self.choice, self.include, self.zeros)
        return interpret_tables(tables, self.include)

    def init_seats_dat(self):
        xs = set()
        for party in self.dat:
            xs.update(set(self.dat[party].keys()))
        if self.choice == 'Canada':
            total_share, all_shares, rel_votes = process_riding_data(get_canada_riding_data())
            seats_dat = {p: {} for p in total_share.keys()}
            for x in xs:
                n = max([len(self.dat[p][x]) if x in self.dat[p] else 0 for p in self.dat])
                for p in total_share:
                    if p == 'IND' or not x < min(self.dat[p]):
                        seats_dat[p][x] = [0 for _ in range(n)]
                for ridata in all_shares.values():
                    for i in range(n):
                        ridat = {}
                        for p in ridata:
                            if p in self.dat and x in self.dat[p] and len(self.dat[p][x]) > i and \
                                    self.dat[p][x][i] is not None:
                                # option A (apply swing proportionally to existing support)
                                new = self.dat[p][x][i] / 100
                                old = total_share[p]
                                ratio = new / old
                                a = ridata[p] * ratio
                                # option B (apply the set percentage swing to every district equally)
                                b = ridata[p] + (self.dat[p][x][i] / 100 - total_share[p]) / rel_votes[p]
                                # option C (use the average of the two)
                                c = (a + b) / 2
                                k = c
                            elif x not in seats_dat[p]:
                                continue
                            else:
                                k = ridata[p]
                            ridat[k] = p
                        p = ridat[max(ridat)]
                        seats_dat[p][x][i] += 1
        elif choices[self.choice]['toggle_seats']:
            seats_dat = {p: {} for p in self.dat}
            for x in xs:
                n = max([len(self.dat[p][x]) if x in self.dat[p] else 0 for p in self.dat])
                for p in self.dat:
                    if x in self.dat[p] and len(self.dat[p][x]) > 0:
                        seats_dat[p][x] = [0 for _ in range(n)]
                for i in range(n):
                    shares = {}
                    inf = choices[self.choice]
                    for p in self.dat:
                        if p in self.dat and x in self.dat[p] and len(self.dat[p][x]) > i and \
                                self.dat[p][x][i] is not None and self.dat[p][x][i] >= inf['threshold']:
                            shares[p] = self.dat[p][x][i]
                        elif x not in seats_dat[p]:
                            continue
                        else:
                            shares[p] = 0
                    if inf['method'] == 'quotient':
                        seatdist = highest_averages_method(shares, inf['seats'], inf['divisor'], inf['bar'])
                    else:
                        seatdist = largest_remainder_method(shares, inf['seats'])
                    for p in seatdist:
                        if x in seats_dat[p]:
                            seats_dat[p][x][i] = seatdist[p]
        else:
            seats_dat = None
        return seats_dat

    @staticmethod
    def dat_ymax(dat):
        try:
            ymax = max([max([max(ys) if len(ys) > 0 else 0 for ys in line.values() if line is not None])
                        for line in dat.values()])
            return ymax * 5 / 4
        except AttributeError:
            return False

    def improve_res(self, resratio):
        if self.metric == 'seats':
            if self.view == 'blocs':
                self.seats_graph_blocs_dat = self.init_graph_data(self.seats_blocs_dat, resratio=resratio)
            elif self.view == 'gov':
                self.seats_graph_gov_dat = self.init_graph_data(self.seats_gov_dat, resratio=resratio)
            else:
                self.seats_graph_dat = self.init_graph_data(self.seats_party_dat, resratio=resratio)
        else:
            if self.view == 'blocs':
                self.graph_blocs_dat = self.init_graph_data(self.blocs_dat, resratio=resratio)
            elif self.view == 'gov':
                self.graph_gov_dat = self.init_graph_data(self.gov_dat, resratio=resratio)
            else:
                self.graph_dat = self.init_graph_data(self.party_dat, resratio=resratio)
        self.make_graph()

    def init_group(self, view, idat):
        if view == 'blocs':
            if self.blocs is None:
                return None
            else:
                relev: Dict = self.blocs
        else:
            if self.gov is None:
                return None
            else:
                relev: Dict = self.gov
        dat = {}
        for b, ps in relev.items():
            dat[b] = {}
            for p in ps:
                for x, ys in idat[p].items():
                    if x in dat[b].keys():
                        for i, y in enumerate(ys):
                            if y is None:
                                continue
                            else:
                                try:
                                    if dat[b][x][i] is None:
                                        dat[b][x][i] = y
                                    else:
                                        dat[b][x][i] += y
                                except IndexError:
                                    dat[b][x].append(y)
                    else:
                        dat[b][x] = ys.copy()
        return dat

    def init_graph_data(self, dat, resratio=7):
        if dat is not None:
            start = min([min(d) for d in dat.values()])
            if self.end_date is None:
                end = 0
            else:
                end = date_kit.date_dif(today, self.end_date)
            limit = 0
            dat = weighted_averages(dat, self.spread, loc=True, resratio=resratio, start=start, end=end, limit=limit)
        return dat

    def make_graph(self):
        if self.to_end_date and self.end_date is not None:
            x_max = date_kit.date_dif(today, self.end_date)
        else:
            x_max = None
        if self.minx == -1:
            x_min = None
        else:
            if x_max is not None:
                end_date = self.end_date
            else:
                end_date = today
            x_min = -date_kit.date_dif(Date(end_date.year - self.minx, end_date.month, end_date.day), today)
        title = "Opinion Polling for " + self.choice

        if self.metric == 'seats':
            if self.view == 'blocs':
                dat = self.seats_graph_blocs_dat
                points = self.seats_blocs_dat
            elif self.view == 'gov':
                dat = self.seats_graph_gov_dat
                points = self.seats_gov_dat
            else:
                dat = self.seats_graph_dat
                points = self.seats_party_dat
            y_title = "Number of Seats"
            intg = True
        else:
            if self.view == 'blocs':
                dat = self.graph_blocs_dat
                points = self.blocs_dat
            elif self.view == 'gov':
                dat = self.graph_gov_dat
                points = self.gov_dat
            else:
                dat = self.graph_dat
                points = self.party_dat
            y_title = "Support (%)"
            intg = False
        y_max = self.dat_ymax(points)
        if y_max is not False:
            graph = GraphDisplay(screen_center, (screen_width, screen_height), dat, x_title=None,
                                 y_title=y_title, title=title, step=1, align=CENTER, colours=self.col,
                                 initial_date=today, leader=True, y_min=0, y_max=y_max, x_max=x_max, x_min=x_min,
                                 dat_points=points, vlines=self.vlines, intg=intg)
            with lock:
                if self.graph is not None:
                    self.graph.hide()
                self.graph = graph
                self.graph.catch(pygame.mouse.get_pos())
                self.graph.show()

    def change_view_or_metric(self):
        if self.dat is None:
            self.dat = filter_trails(self.init_dat())
            self.party_dat = filter_nils(copy.deepcopy(self.dat))
        if self.metric == 'seats':
            if self.seats_party_dat is None:
                self.seats_party_dat = self.init_seats_dat()
            if self.view == 'blocs' and self.seats_graph_blocs_dat is None:
                if self.seats_blocs_dat is None:
                    self.seats_blocs_dat = filter_nils(self.init_group(self.view, self.seats_party_dat))
                self.seats_graph_blocs_dat = self.init_graph_data(self.seats_blocs_dat, resratio=self.low_res)
            elif self.view == 'gov' and self.seats_graph_gov_dat is None:
                if self.seats_gov_dat is None:
                    self.seats_gov_dat = filter_nils(self.init_group(self.view, self.seats_party_dat))
                self.seats_graph_gov_dat = self.init_graph_data(self.seats_gov_dat, resratio=self.low_res)
            elif self.view == 'parties' and self.seats_graph_dat is None:
                self.seats_graph_dat = self.init_graph_data(self.seats_party_dat, resratio=self.low_res)
        else:
            if self.view == 'blocs' and self.graph_blocs_dat is None:
                if self.blocs_dat is None:
                    self.blocs_dat = filter_nils(self.init_group(self.view, self.dat))
                self.graph_blocs_dat = self.init_graph_data(self.blocs_dat, resratio=self.low_res)
            elif self.view == 'gov' and self.graph_gov_dat is None:
                if self.gov_dat is None:
                    self.gov_dat = filter_nils(self.init_group(self.view, self.dat))
                self.graph_gov_dat = self.init_graph_data(self.gov_dat, resratio=self.low_res)
            elif self.view == 'parties' and self.graph_dat is None:
                self.graph_dat = self.init_graph_data(self.party_dat, resratio=self.low_res)
        self.make_graph()
        thread = threading.Thread(target=self.improve_res, args=(self.high_res,))
        thread.start()

    def change_view(self, view):
        self.view = view
        self.change_view_or_metric()

    def change_metric(self, metric):
        self.metric = metric
        self.change_view_or_metric()

    def change_spread(self, button):
        if button == self.up_spread:
            self.down_spread.enable()
            self.spread += 10
            if self.spread >= 360:
                self.spread = 360
                self.up_spread.disable()
        elif button == self.down_spread:
            self.up_spread.enable()
            self.spread -= 10
            if self.spread <= 10:
                self.spread = 10
                self.down_spread.disable()
        self.spread_txt.update(str(self.spread))
        self.graph_dat = None
        self.graph_blocs_dat = None
        self.graph_gov_dat = None
        self.seats_graph_dat = None
        self.seats_gov_dat = None
        self.seats_blocs_dat = None
        self.change_view_or_metric()

    def change_minx(self, minx):
        self.minx = minx
        self.make_graph()

    def change_toend(self, toend):
        self.to_end_date = toend
        self.make_graph()


class MenuPage:

    def __init__(self, options):
        button_size = 64
        self.notices = {}
        self.display = ScrollButtonDisplay((screen_rect.centerx, screen_rect.top + screen_height / 16),
                                           (400, screen_height * 3 / 4), button_size * len(options),
                                           align=TOP, button_size=button_size)
        background_colour = dark_grey
        for i, entry in enumerate(options):
            b = Button((self.display.contain_rect.left, self.display.contain_rect.top + i * button_size),
                       (self.display.contain_rect.w, button_size), parent=self.display)
            b.callback(functools.partial(GraphPage, entry, to_end_date=True))
            img_path = 'images/flags/' + entry.lower() + '.png'
            try:
                img = Image((b.rect.centerx + b.rect.w / 8, b.rect.centery), (b.rect.w * 3 / 8, b.rect.h * 3 / 4),
                            img_path, align=LEFT)
                b.components.append(img)
            except FileNotFoundError:
                pass
            label = Text(entry.upper(), (b.rect.centerx + b.rect.w / 16, b.rect.centery + b.rect.h / 12), 24,
                         align=BOTTOMRIGHT,
                         background_colour=background_colour)
            b.components.append(label)
            if choices[entry]['end_date'] is None:
                txt = 'Unknown'
            else:
                txt = str(choices[entry]['end_date'])
            date = Text(txt, label.rect.bottomright, align=TOPRIGHT, background_colour=background_colour)
            b.components.append(date)
            self.display.components.append(b)
            self.display.button_tags[entry] = b

        self.update_b = Button((screen_rect.centerx, screen_height * 7 / 8), align=CENTER, label='Update Data')
        self.update_b.callback(update_data)

        self.close_b = close_button()

        self.show()

    def show(self):
        if threading.active_count() == 1:
            widgets.clear()
            self.display.show()
            self.update_b.show()
            self.close_b.show()
            self.update_notices()

    def update_notices(self):
        for tag in updated:
            if tag not in self.notices:
                b = self.display.button_tags[tag]
                img_path = 'images/exclamation.png'
                img = Image((b.rect.left, b.rect.centery), (b.rect.h * 2 / 3, b.rect.h / 2),
                            img_path, align=LEFT)
                self.notices[tag] = img
                b.components.append(img)


def get_canada_riding_data():
    try:
        with open('misc_data/ridings.csv', 'r') as f:
            doc = csv.reader(f)
            dat: Dict[str, List[Dict[str, Any]]] = {}
            region = None
            for i, row in enumerate(doc):
                if i == 0:
                    keys = row
                else:
                    if row[1] != region:
                        region = row[1]
                        dat[region] = []
                    riding = {}
                    for j, k in enumerate(keys):
                        v = row[j]
                        if k == 'turnout':
                            v = float(v)
                        elif j >= 4:
                            if v == '':
                                v = 0
                            else:
                                v = int(v)
                        riding[k] = v
                    dat[region].append(riding)
            return dat
    except FileNotFoundError:
        raise FileNotFoundError('Could not find ridings.csv in data folder')


def remove_from_update(tag):
    if tag in updated:
        updated.remove(tag)
        menu_page.display.button_tags[tag].components.remove(menu_page.notices[tag])
        menu_page.notices.pop(tag)
        update_save()


def update_save():
    s = ''
    for tag in updated:
        s += tag + ','
    s = s[:-1]
    with open(save_loc, 'w') as f:
        f.write(s)


def update_data(sel="All"):
    global today

    def update_dat(dest, url, tag):
        try:
            content = urllib.request.urlopen(url)
            read_content = content.read()
            soup = BeautifulSoup(read_content, 'html.parser')
            content = soup.find_all('textarea')
            text = content[0].text
            final = text.encode('utf-8')
            try:
                with open(dest, 'rb') as rf:
                    old_text = rf.read()
                    if old_text != final and tag not in updated:
                        updated.append(tag)
            except FileNotFoundError:
                updated.append(tag)
            with open(dest, 'wb') as wf:
                wf.write(final)
        except urllib.error.URLError:
            print('Failed to load for ' + tag + ' from ' + url)

    today = get_today()
    if sel == 'All':
        threads = []
        old_updated = updated.copy()
        for tag in choices:
            if 'url' in choices[tag]:
                url = choices[tag]['url']
                dest = choices[tag]['file_name']
                thread = threading.Thread(target=update_dat, args=(dest, url, tag))
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.join()
        if updated != old_updated:
            update_save()
        menu_page.update_notices()


def process_riding_data(dat):
    tags = ['LIB', 'CON', 'NDP', 'BQ', 'GRN', 'PPC', 'IND']
    total_votes = {p: 0 for p in tags}
    rel_votes = total_votes.copy()
    all_shares = {}
    for region in dat:
        for riding in dat[region]:
            totloc = 0
            for party in total_votes:
                v = riding[party]
                total_votes[party] += v
                totloc += v
            all_shares[riding['name']] = {p: riding[p] / totloc for p in total_votes}
            for party in rel_votes:
                if riding[party] > 0:
                    rel_votes[party] += totloc
    tot = sum(total_votes.values())
    rel_votes = {p: rel_votes[p] / tot for p in rel_votes}
    total_share = {p: total_votes[p] / tot for p in total_votes}
    return total_share, all_shares, rel_votes


def sort_choices(choices):
    def sorter(c):
        return choices[c]['end_date'].numerate()

    order = []
    prevs = []
    nones = []
    for c in choices:
        if choices[c]['end_date'] is None:
            nones.append(c)
        else:
            num = sorter(c)
            if num < today.numerate():
                prevs.append(c)
            else:
                order.append(c)
    order.sort(key=sorter)
    prevs.sort(key=sorter, reverse=True)
    nones.sort()
    return order + prevs + nones


def close_button():
    dim = screen_height / 40
    m = dim * 3 / 4
    c = (200, 20, 20)
    b = Button((screen_width, 0), (dim, dim), align=TOPRIGHT, threed=False, colour=c)
    surf = pygame.Surface((m, m))
    surf.fill(white)
    surf.set_colorkey(white)
    pygame.draw.line(surf, gold, (0, 0), (m, m), width=3)
    pygame.draw.line(surf, gold, (0, m), (m, 0), width=3)
    cross = Widget(b.rect.center, (m, m), align=CENTER, surface=surf, catchable=False)
    b.components.append(cross)
    b.callback(quit)
    b.show()
    return b


def get_today():
    tod = str(datetime.date.today())
    year, month, day = tod.split('-')
    today = Date(int(year), int(month), int(day))
    return today


today = get_today()


if __name__ == '__main__':
    save_loc = 'updated.txt'
    updated: List
    try:
        with open(save_loc, 'r') as f:
            updated = f.read().split(',')
            if updated == ['']:
                updated = []
    except FileNotFoundError:
        updated = []
    choices = choices_setup()
    lock = threading.Lock()
    order = sort_choices(choices)
    menu_page = MenuPage(order)
    surface = pygame.Surface((screen_width, screen_height))
    surface.fill(whitish)

    pygame.display.set_caption('Polling')
    icon = pygame.transform.scale((pygame.image.load("images/graph.png")), (32, 32))
    icon_surf = pygame.Surface((32, 32))
    icon_surf.fill(white)
    icon_surf.blit(icon, (0, 0), None)
    pygame.display.set_icon(icon_surf)
    run_loop(lock, background=surface, escape=False)
