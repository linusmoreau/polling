from base_ui import *
from toolkit import *
import date_kit
import types
import datetime
import urllib.request
import urllib.error
import threading
import csv
from country_data import specs
from bs4 import BeautifulSoup
from os.path import exists


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
        if len(ns) > 1 and ns[0] == '!':
            ns = '|' + ns[1:]
        s += ns
    content = s.split('||')
    ncontent = []
    j = 0
    while j < len(content) - 1:
        line = content[j].strip()
        if line == '-' and len(content[j].strip('\n')) > 1:
            line = '–'
        for p in range(len(line) - 2):
            if line[p:p + 2] == '{{' and '}}' not in line[p + 2:]:
                j += 1
                line += '|' + content[j].strip()
                while '}}' not in content[j]:
                    j += 1
                    line += '|' + content[j].strip()
                break
        ncontent.append(line)
        j += 1
    ncontent.append(content[-1])
    content = ncontent

    found = False
    ignore = False
    while i < len(content):
        line = content[i].strip('| \n')
        if line == '-' and len(content[i].strip('|\n')) > 1:
            line = '–'
        nkey = []
        if choice == 'Russia':
            if 'Old Russia' in line:
                nkey = ['date', 'firm',
                        'UR', 'CPRF', 'LDPR', 'SRZP',
                        'CR', 'Yabloko', 'RRPSJ', 'Rodina', 'PG', 'Greens', 'CP', 'RPFJ', 'NP', 'GA',
                        'Undecided', 'Abstention',
                        'lead', 'end']
            if 'Pre-campaign 2021' in line:
                nkey = ['date', 'firm',
                        'UR', 'CPRF', 'LDPR', 'SRZP', 'Other', 'Undecided', 'Abstention',
                        'lead', 'end']
        elif choice == 'Canada':
            if 'Opinion polling during the campaign period of 2019 Canadian federal election' in line:
                nkey = ['firm', 'date', 'link',
                        'LPC', 'CPC', 'NDP', 'BQ', 'GPC', 'PPC',
                        'margin', 'size', 'method', 'lead', 'end']
            elif 'Opinion polling during the campaign period of the 2021 Canadian federal election' in line:
                nkey = ['firm', 'date', 'link',
                        'CPC', 'LPC', 'NDP', 'BQ', 'GPC', 'PPC',
                        'Other', 'margin', 'size', 'method', 'lead']
        elif choice == 'Brazil':
            mark = 'https://tribunapr.uol.com.br/noticias/brasil/bolsonaro-e-lula-empatam-na-pesquisa-exame-' \
                   'ideia-para-as-eleicoes-2022/'
            if mark in line:
                nkey = ['firm', 'date', 'sample',
                        'Bolsonaro (PL)', 'Lula (PT)', 'Haddad (PT)', 'Dino (PCdoB)', 'Gomes (PDT)', 'Boulos (PSOL)',
                        'Doria (PSDB)', 'Amoedo (NOVO)', 'Moro (PODE)', 'Huck',
                        'Other', 'Undecided', 'lead', 'end']
            if '====2019====' in line:
                nkey = ['firm', 'date', 'sample',
                        'Bolsonaro (PL)', 'Lula (PT)', 'Haddad (PT)', 'Gomes (PDT)', 'Doria (PSDB)', 'Amoedo (NOVO)',
                        'Moro (PODE)', 'Huck',
                        'Other', 'Undecided', 'lead', 'end']
            elif '====2021====' in line:
                nkey = ['firm', 'date', 'sample',
                        'Bolsonaro (PL)', 'Lula (PT)', 'Moro (PODE)', 'Gomes (PDT)', 'Doria (PSDB)',
                        'Leite (PSDB)', 'Mandetta (DEM)', 'Pancheco (DEM)',
                        'Other', 'Undecided', 'lead', 'end']
            elif 'Jan–Mar' in line:
                nkey = ['firm', 'date', 'sample',
                        'Bolsonaro (PL)', 'Lula (PT)', 'Moro (PODE)', 'Gomes (PDT)', 'Doria (PSDB)',
                        'Other', 'Undecided', 'lead']
            elif 'Apr–Jun' in line:
                nkey = ['firm', 'date', 'sample',
                        'Bolsonaro (PL)', 'Lula (PT)', 'Gomes (PDT)', 'Doria (PSDB)',
                        'Other', 'Undecided', 'lead']
        elif choice == 'Italy':
            if not found and '[https://sondaggibidimedia.com/politiche-sondaggio-swg-8-agosto/ SWG]' in line:
                nkey = ['date', 'firm', 'sample',
                        'M5S', 'PD', 'Lega', 'FI', 'FdI', 'Art.1', 'AVS', 'AVS', '+E-A', 'IV', 'Italexit', 'IC',
                        'Other', 'lead', 'end']
                found = True
                i -= 1
            elif '=== 2022 ===' in line:
                nkey = ['date', 'firm', 'sample',
                        'FdI', 'PD', 'M5S', 'Lega', 'FI', 'A-IV', 'AVS', '+E', 'Italexit', 'UP', 'ISP', 'NM',
                        'other', 'lead']
            elif '=== Pre-election 2022 ===' in line:
                nkey = ['date', 'firm', 'sample',
                        'M5S', 'PD', 'Lega', 'FI', 'FdI', 'AVS', '+E', 'A-IV', 'Italexit', 'IC', 'NM',
                        'other', 'lead', 'end']
            elif '=== 2021 ===' in line:
                nkey = ['date', 'firm', 'sample',
                        'M5S', 'PD', 'Lega', 'FI', 'FdI', 'Art.1', 'SI', '+Eu', 'EV', 'A', 'IV', 'CI',
                        'Other', 'lead', 'end']
            elif 'Polling program mark: May 2021' in line:
                nkey = ['date', 'firm', 'sample',
                        'M5S', 'PD', 'Lega', 'FI', 'FdI', 'LeU', '+Eu', 'EV', 'C!', 'A', 'IV',
                        'Other', 'lead', 'end']
            elif 'Polling program mark: April 2019' in line:
                nkey = ['date', 'firm', 'sample',
                        'M5S', 'PD', 'Lega', 'FI', 'FdI', 'LeU', '+Eu', 'NcI', 'PaP',
                        'Other', 'lead', 'end']
        elif choice == 'Germany':
            if 'Old Germany' in line:
                nkey = ['firm', 'date', 'sample', 'abs',
                        'Union', 'SPD', 'AfD', 'FDP', 'Linke', 'Gr\u00fcne',
                        'FW', 'Other', 'lead', 'end']
            elif '=== 2020 ===' in line:
                nkey = ['firm', 'date', 'sample', 'abs',
                        'Union', 'SPD', 'AfD', 'FDP', 'Linke', 'Gr\u00fcne',
                        'Other', 'lead', 'end']
        elif choice == 'Japan':
            if '=== 2020 ===' in line:
                nkey = ['date', 'firm',
                        'LDP', 'CDP', 'NKP', 'JCP', 'Ishin', 'DPP', 'SDP', 'Reiwa', 'Kibo', 'NHK',
                        'Other', 'None', 'lead', 'end']
        elif choice == 'Estonia':
            if '[[Kaja Kallas\' cabinet]] is formed by the Reform Party and Centre Party' in line:
                nkey = ['firm', 'date', 'sample',
                        'Reform', 'Centre', 'EKRE', 'Isamaa', 'SDE', 'E200', 'Green', 'TULE/EVA',
                        'Other', 'lead', 'gov', 'opp', 'end']
            if '=== 2020 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'Reform', 'Centre', 'EKRE', 'Isamaa', 'SDE', 'E200', 'Green', 'TULE/EVA',
                        'Other', 'lead', 'gov', 'opp', 'end']
        elif choice == 'Poland':
            if '=== 2022 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'United Right', 'Agreement', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Kukiz\'15',
                        'Confederation', 'Poland 2050', 'AGRO unia',
                        'Other', 'lead']
            elif '=== 2020 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'United Right', 'Civic Coalition', 'Civic Coalition', 'The Left', 'Polish Coalition',
                        'Kukiz\'15', 'Confederation', 'Poland 2050',
                        'Other', 'lead', 'end']
            elif '=== 2019 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'United Right', 'Civic Coalition', 'The Left', 'Polish Coalition', 'Confederation',
                        'Other', 'lead', 'end']
        elif choice == 'Austria':
            if '=== By state ===' in line:
                break
        elif choice == 'Ireland':
            if '==National opinion polls==' in line:
                nkey = ['date', 'firm', 'sample',
                        'FG', 'FF', 'SF', 'Lab', 'PBP/S', 'SD', 'GP', 'O/I', 'O/I', 'O/I',
                        'end']
        elif choice == 'Netherlands':
            if '{{For|events during those years|2020 in the Netherlands|2019 in the Netherlands|' \
               '2018 in the Netherlands|2017 in the Netherlands}}' in line:
                nkey = ['firm', 'date',
                        'VVD', 'PVV', 'CDA', 'D66', 'GL', 'SP', 'PvdA', 'CU', 'PvdD', '50+', 'SGP', 'DENK', 'FVD',
                        'JA21', 'Volt', 'BIJ1', 'BBB',
                        'Others', 'lead', 'end']
        elif choice == 'Bulgaria':
            if 'Pre-November 2021 election' in line:
                nkey = ['firm', 'date', 'sample', 'turnout', 'Undecided',
                        'ITN', 'GERB', 'BSP', 'DB', 'DPS', 'IBG-NI', 'IMRO', 'Revival', 'PP',
                        'Other', 'None', 'lead']
            elif 'Pre-2022 election' in line:
                nkey = ['firm', 'date', 'sample',
                        'PP', 'DB', 'GERB', 'DPS', 'BSP', 'ITN', 'Revival', 'IBG-NI', 'IMRO', 'BV',
                        'Other', 'None', 'lead']
            elif 'https://bntnews.bg/news/parvi-prognozni-rezultati-6-partii-vlizat-v-parlamenta-stotni-' \
                 'delyat-gerb-i-itn-1162099news.html' in line:
                nkey = ['firm', 'date', 'sample',
                        'GERB', 'ITN', 'BSP', 'DPS', 'DB', 'IBG-NI', 'BP', 'BP', 'BP', 'Revival', 'BL', 'RzB',
                        'LSChSR',
                        'Other', 'lead', 'end']
            elif 'Pre-April Election polls' in line:
                nkey = ['firm', 'date', 'sample', 'moe',
                        'GERB', 'BSP', 'DPS', 'BP', 'DB', 'Volya', 'ITN', 'IBG-NI',
                        'Other', 'lead', 'end']
            elif 'announce that they will run together' in line:
                nkey = ['firm', 'date', 'sample',
                        'GERB', 'PP', 'DB', 'DPS', 'Revival', 'BSP', 'BV', 'IMRO', 'ITN', 'IBG-NI', 'NDSV',
                        'Other', 'None', 'lead']
        elif choice == 'Norway':
            if 'Old Norway' in line:
                nkey = ['firm', 'date', 'sample', 'resp',
                        'R', 'SV', 'MDG', 'Ap', 'Sp', 'V', 'KrF', 'H', 'FrP',
                        'Other', 'lead', 'end']
        elif choice == 'Chile':
            if '=== Before official registration of candidates ===' in line:
                nkey = ['date', 'firm', 'type',
                        'Jiles', 'Jadue', 'Boric', 'Sanchez', 'Enriquez-Om.', 'Guiller', 'Bachelet', 'Narvaez', 'Munoz',
                        'Vidal', 'Maldonado', 'Provoste', 'Rincon', 'Sichel', 'F. Kast', 'Briones', 'Desbordes',
                        'Pinera', 'Lavin', 'Matthei', 'Kast', 'Parisi', 'Farkas', 'Siches',
                        'Other', 'end']
            elif '==First round==' in line:
                nkey = ['date', 'source', 'type',
                        'Artes', 'Boric', 'Enriquez-Om.', 'Provoste', 'Parisi', 'Sichel', 'Kast',
                        'Other', 'end']
        elif choice == 'Latvia':
            if 'A new party - [[Law and Order (Latvia)|LuK]] - is established' in line:
                nkey = ['firm', 'date', 'sample', 'dec',
                        'S', 'PCL', 'JKP', 'AP!', 'NA', 'ZZS', 'JV', 'LRA', 'LKS', 'P',
                        'Other', 'lead', 'gov', 'opp', 'end']
            elif 'Two new parties - [[Latvia First]] and [[Republic (Latvia)|Republic]] - are established' in line:
                nkey = ['firm', 'date', 'sample', 'dec',
                        'S', 'PCL', 'JKP', 'AP!', 'NA', 'ZZS', 'JV', 'LRA', 'LKS', 'P', 'LuK',
                        'Other', 'lead', 'gov', 'opp', 'end']
        elif choice == 'Denmark':
            if 'Pre-election 2022' in line:
                nkey = ['firm', 'date', 'sample',
                        'A', 'V', 'O', 'B', 'F', '\u00d8', 'C', '\u00c5', 'D', 'I', 'K', 'G', 'M', 'Q', 'Æ',
                        'Other', 'red', 'blue', 'leadall', 'leadabove']
            elif '=== 2021 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'A', 'V', 'O', 'B', 'F', '\u00d8', 'C', '\u00c5', 'D', 'I', 'P', 'K', 'E', 'G', 'M', 'Q',
                        'Other', 'lead', 'red', 'blue', 'lead']
            elif '=== 2020 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'A', 'V', 'O', 'B', 'F', '\u00d8', 'C', '\u00c5', 'D', 'I', 'P', 'K', 'E', 'G',
                        'Other', 'lead', 'red', 'blue', 'lead']
            elif '=== 2019 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'A', 'V', 'O', 'B', 'F', '\u00d8', 'C', '\u00c5', 'D', 'I', 'P', 'K', 'E', 'G',
                        'Other', 'lead', 'red', 'blue', 'lead']
        elif choice == 'France Prez':
            if '=== March ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'Arthaud', 'Poutou', 'Roussel', 'Mélenchon', 'Taubira', 'Hidalgo', 'Jadot', 'Thouy',
                        'Macron', 'Lassalle', 'Pécresse', 'Dupont-Aignan', 'Le Pen', 'Zemmour', 'Asselineau',
                        'end']
            elif '=== February ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'Arthaud', 'Poutou', 'Roussel', 'Mélenchon', 'Taubira', 'Hidalgo', 'Jadot', 'Thouy',
                        'Macron', 'Pécresse', 'Lassalle', 'Dupont-Aignan', 'Le Pen', 'Philippot', 'Zemmour',
                        'Asselineau',
                        'end']
            elif '==== January ====' in line:
                nkey = ['firm', 'date', 'sample',
                        'Arthaud', 'Poutou', 'Roussel', 'Mélenchon', 'Taubira', 'Montebourg', 'Hidalgo', 'Thouy',
                        'Jadot', 'Macron', 'Pécresse', 'Dupont-Aignan', 'Lassalle', 'Le Pen', 'Philippot', 'Zemmour',
                        'Asselineau',
                        'end']
            elif '==== September–November ====' in line:
                nkey = ['firm', 'date', 'sample',
                        'Arthaud', 'Poutou', 'Roussel', 'Mélenchon', 'Montebourg', 'Hidalgo', 'Jadot', 'Macron',
                        'Lagarde',
                        'Barnier', 'Bertrand', 'Ciotti', 'Juvin', 'Payre', 'Pécresse', 'Poisson',
                        'Dupont-Aignan', 'Lassalle',
                        'Le Pen', 'Philippot', 'Zemmour', 'Asselineau',
                        'end']
            elif '==== January–September ====' in line:
                nkey = ['firm', 'date', 'sample',
                        'Arthaud', 'Poutou', 'Roussel', 'Mélenchon', 'Montebourg', 'Hidalgo', 'Hollande', 'Piolle',
                        'Jadot', 'Macron', 'Lagarde', 'Bertrand', 'Pécresse', 'Barnier', 'Baroin',
                        'Retailleau', 'Wauquiez', 'Poisson', 'Dupont-Aignan', 'Lassalle', 'Le Pen', 'Zemmour',
                        'Asselineau',
                        'end']
            elif '=== 2017–2020 ===' in line:
                nkey = ['firm', 'date', 'sample',
                        'Arthaud', 'Poutou', 'Roussel', 'Mélenchon', 'Hamon', 'Cazeneuve', 'Faure', 'Hidalgo',
                        'Hollande', 'Royal', 'Jadot', 'Macron', 'Lagarde', 'Bertrand', 'Pécresse',
                        'Baroin', 'Dati', 'Fillon', 'Retailleau', 'Wauquiez', 'Dupont-Aignan', 'Lassalle', 'Le Pen',
                        'Asselineau', 'Cheminade',
                        'end']
        elif choice == 'Portugal':
            if '====Hypothetical scenarios====' in line:
                ignore = True
            elif 'Old Polling' in line:
                ignore = False
                nkey = ['firm', 'date', 'sample', 'turnout',
                        'PS', 'PSD', 'BE', 'CDU', 'CDS-PP', 'PAN', 'Chega', 'IL', 'LIVRE',
                        'Other', 'lead']
        elif choice == 'Spain':
            if '===2020===' in line:
                nkey = ['firm', 'date', 'sample', 'turnout',
                        'PSOE', 'PP', 'VOX', 'UP', 'Cs', 'ERC', 'MP', 'JxCat', 'PNV', 'EHB', 'CUP', 'CC', 'BNG', 'NA+',
                        'PRC', 'TE', 'lead', 'end']
            elif '2023 (before Sumar)' in line:
                nkey = ['firm', 'date', 'sample', 'turnout',
                        'PSOE', 'PP', 'VOX', 'UP', 'Cs', 'ERC', 'MP', 'JxCat', 'PNV', 'EHB', 'CUP', 'CC', 'BNG', 'NA+',
                        'PRC', 'EV', 'lead', 'end']
        elif choice == 'Slovenia':
            if 'Parties which ran in 2018' in line:
                nkey = ['date', 'firm', 'publisher', 'sample',
                        'SDS', 'LMS', 'SD', 'K', 'Left', 'NSi', 'SAB', 'DeSUS', 'SNS', 'SLS', 'PPS', 'DD', 'ACZS',
                        'Other', 'None', 'Undecided', 'Abstain', 'lead', 'source', 'end']
            elif '===Scenario Polls===' in line:
                break
            elif 'Pre-2022' in line:
                nkey = ['date', 'firm', 'publisher', 'sample',
                        'SDS', 'LMS', 'SD', 'K', 'K', 'Left', 'NSi', 'SAB', 'DeSUS', 'SNS', 'PPS', 'DD', 'ND',
                        'GS', 'GS', 'Vesna', 'Res.', 'LIDE',
                        'Other', 'None', 'Undecided', 'Abstain', 'lead', 'source', 'end']
        elif choice == 'Romania':
            if '=== 2021 ===' in line:
                nkey = ['date', 'source', 'sample',
                        'PSD', 'PNL', 'FD', 'USR', 'AUR', 'UDMR', 'PMP', 'PRO', 'ALDE', 'PPU-SL', 'PER', 'APP',
                        'Other', 'lead', 'end']
        elif choice == 'Costa Rica':
            if 'Second round' in line:
                nkey = ['date', 'firm', 'Chaves', 'Figueres', 'Other', 'end']
        elif choice == 'Israel':
            if 'url=https://www.ynetnews.com/article/nozaf2n25' in line:
                nkey = ['date', 'firm', 'publisher',
                        'Likud', 'Yesh Atid', 'Shas', 'Blue & White', 'Yamina', 'Labor', 'UTJ', 'Yisrael Beitenu',
                        'Religious Zionist', 'Joint List', 'New Hope', 'Meretz', 'Ra\'am',
                        'gov', 'end']
        elif choice == 'Iceland':
            if '== Pre-2021 ==' in line:
                nkey = ['firm', 'date', 'sample', 'resp',
                        'D', 'V', 'S', 'M', 'B', 'P', 'F', 'C', 'J',
                        'Other', 'lead', 'end']
        elif choice == 'Czechia':
            if '=== 2021 ===' in line:
                nkey = ['firm', 'date', 'size', 'turnout',
                        'ANO', 'SPOLU', 'SPOLU', 'SPOLU', 'PaS', 'PaS', 'SPD', 'KSCM', 'CSSD', 'T-S',
                        'T-S', 'Z', 'APB', 'VB', 'P',
                        'Other', 'Lead', 'Govt.', 'Opp.']
        elif choice == 'Turkey':
            if 'https://www.cumhuriyet.com.tr/amp/siyaset/' \
               'son-dakika-deva-gelecek-saadet-ve-demokrat-parti-secime-chp-listesinden-girecek-2068710' in line:
                nkey = ['date', 'firm', 'sample',
                        'AKP', 'MHP', 'BBP', 'YRP', 'People\'s Alliance',
                        'CHP', 'IYI', 'SP', 'DEVA', 'GP', 'DP', 'Nation Alliance',
                        'HDP', 'TIP', 'Labour and Freedom',
                        'ZP', 'MP', 'TDP', 'BTP', 'other', 'lead']
            if '===2022===' in line:
                nkey = ['date', 'firm', 'size',
                        'AKP', 'CHP', 'HDP', 'MHP', 'IYI', 'SP', 'DEVA', 'GP', 'BBP', 'YRP', 'MP', 'TDP', 'DP', 'TIP',
                        'ZP', 'BTP', 'other', 'lead']
            elif '===2020===' in line:
                nkey = ['date', 'firm', 'size',
                        'AKP', 'CHP', 'HDP', 'MHP', 'IYI', 'SP', 'DEVA', 'GP', 'BBP', 'YRP', 'MP', 'other', 'lead']
            elif '===2019===' in line:
                nkey = ['date', 'firm', 'size',
                        'AKP', 'CHP', 'HDP', 'MHP', 'IYI', 'SP', 'DEVA', 'GP', 'BBP', 'YRP', 'other', 'lead']
            elif '===2018===' in line:
                nkey = ['date', 'firm', 'size',
                        'AKP', 'CHP', 'HDP', 'MHP', 'IYI', 'SP', 'other', 'lead']
        elif choice == 'Alberta':
            if '===Regional polls===' in line:
                break
        if not ignore:
            if len(nkey) > 0:
                tables.append({'table': table[:], 'key': key, 'years': years})
                table = []
                years = {0: years[max(years)]}
                row = 0
                col = 0
                key = nkey
            cont = False
            if len(line) > 0 and line[0] == '}':
                started = False
                col = 0
                row += 1
                cont = True
            if '==' in line and '[' not in line:
                yline = line[line.find('=='):]
                yline = yline.strip('= \n')[:4]
                try:
                    int(yline)
                except ValueError:
                    pass
                else:
                    years[row] = yline
                col = 0
                started = False
                cont = True
            if cont:
                i += 1
                continue
            if not started:
                for b in begin:
                    if b in line:
                        started = True
                        i += start
                        line = content[i].strip('| \n')
                        break
            if started:
                if len(line) > 0 and line[0] == '-':
                    if col != 0:
                        col = 0
                        row += 1
                    i += 1
                    continue
                if len(table) <= row:
                    placeholder = [True for _ in range(len(key))]
                    table.extend([placeholder.copy() for _ in range(row - len(table) + 1)])
                # if len(line) > 0 and col == 0 and line[0] == '-':
                #     i += 1
                #     continue
                while table[row][col] is False:
                    col += 1
                    if col >= len(key):
                        col -= len(key)
                        row += 1
                        if len(table) <= row:
                            placeholder = [True for _ in range(len(key))]
                            table.extend([placeholder.copy() for _ in range(row - len(table) + 1)])
                # if len(line) > 0 and col == 0 and line[0] == '-':
                #     i += 1
                #     continue
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
                    num = int(temp.strip('|= ').split()[0].split('|')[0].strip('"{}N/A ').split('"')[0])
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
    def process_date(line: string, year) -> Optional[int]:
        line = line.strip().strip('}\'')
        if '<br>' in line:
            place = line.find('<br>')
            line = line[:place] + ' ' + line[place + 4:]
        if choice in ['UK', 'Germany', 'Netherlands', 'Italy'] and 'opdrts' in line.lower():
            temp = line.strip('|').split('|')
            if temp[-1] == 'year':
                shift = True
            else:
                shift = False
            y = temp[-1 - shift]
            m = temp[-2 - shift]
            d = temp[-3 - shift]
            temp = d + ' ' + m + ' ' + y
        elif choice == 'Norway' and ('dts' in line or 'opdrts' in line):
            temp = line.strip('}|').split('|')
            y = temp[-1]
            m = temp[-2]
            d = temp[-3]
            temp = d + ' ' + m + ' ' + y
        elif choice == 'Ireland' and 'dts' in line:
            temp = line.strip('}|').split('|')
            d = temp[-1]
            m = temp[-2]
            y = temp[-3]
            temp = d + ' ' + m + ' ' + y
        elif choice == 'Alberta':
            if 'dts' in line:
                line = line[line.find('dts'):]
                temp = line.strip('}|').split('|')
                temp2 = temp[-1].split(',')
                y = temp2[-1].strip()
                temp3 = temp[1].split()
                d = temp3[1].strip(',"')
                m = temp3[0]
                temp = d + ' ' + m + ' ' + y
            else:
                temp = line.split(',')
                y = temp[-1].strip()
                temp2 = temp[0].split()
                m = temp2[0]
                d = temp2[1].split('–')[0]
                temp = d + ' ' + m + ' ' + y
        else:
            if '{{efn' in line:
                line = line[:line.find('{{efn')]
            if '<!' in line:
                line = line[:line.find('<!')]
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
                temp = str(date_kit.get_month_length(date_kit.get_month_number(temps[0]), int(year))) + \
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
        elif choice == 'Costa Rica':
            temp = temp.split(":")[-1]
        temp = temp.split('|')[-1].strip()
        temp = temp.replace(',', '.')
        if temp in ['â€“', '-', '', '–', '—'] or "small" in temp:
            if choice == 'Israel':
                share = 0
            else:
                share = None
        else:
            try:
                share = float(temp.strip().strip("'%!\"}"))
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
            if date is False and choice in ["Spain"]:
                for j in range(i - 1, -1, -1):
                    t = table[j][date_i]
                    if type(t).__name__ == 'int' and t < 0:
                        date = t
                        break
            else:
                remove.append(i)
                continue
        else:
            try:
                date = process_date(entry[date_i], year)
            except KeyError:
                print("Error processing date")
                date = None
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
            if k in include and entry[i] is not None and entry[i] != 0 and entry[i] != 1:
                count += 1
                if count > 1:
                    break
        else:
            purge.add(r)
    if choice == 'Czechia':
        for p in ['SPOLU', 'PaS']:
            c = key.count(p)
            if c > 1:
                i = key.index(p)
                for j in range(1, c):
                    for k, entry in enumerate(table):
                        if entry[i + j] is not None:
                            purge.add(k)
        for p in ['ODS', 'STAN']:
            c = key.count(p)
            if c > 0:
                i = key.index(p)
                for k, entry in enumerate(table):
                    if entry[i + 1] is None:
                        purge.add(k)
    elif choice == 'Brazil':
        i = key.index('firm')
        for k, entry in enumerate(table):
            if type(entry[i]).__name__ == 'str':
                if '2018 Brazilian general election' in entry[i]:
                    purge.add(k)
    elif choice == 'France':
        i = key.index('firm')
        j = key.index('LR')
        for k, entry in enumerate(table):
            if type(entry[i]).__name__ == 'str':
                if '2017 election' in entry[i]:
                    purge.add(k)
            elif entry[j] is None:
                purge.add(k)
    elif choice == 'Spain':
        for p in ('PSOE', 'UP'):
            i = key.index(p)
            for k, entry in enumerate(table):
                if entry[i] is None:
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
            for fig in entry[i:i + 3]:
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
    elif choice == 'France Prez':
        for p in ['Mélenchon', 'Hidalgo', 'Jadot', 'Macron', 'Pécresse', 'Le Pen']:
            i = key.index(p)
            for k, entry in enumerate(table):
                if entry[i] is None:
                    purge.add(k)
    elif choice == 'Chile':
        if len(key) <= 8:
            i = key.index('date')
            for k, entry in enumerate(table):
                if entry[i] < date_kit.date_dif(today, Date(2021, 11, 21)):
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
    def set_default_colours_blocs():
        for line in d['blocs'].keys():
            if line not in d['col']:
                d['col'][line] = d['col'][d['blocs'][line][0]]

    def set_default_colours_gov():
        if type(d['gov']).__name__ == 'list':
            for period in d['gov']:
                for group in period.groups:
                    if group.colour is None:
                        group.colour = d['col'][group.parties[0]]
                    d['col'][group.name] = group.colour
        else:
            for line in d['gov'].keys():
                if line not in d['col'].keys():
                    d['col'][line] = d['col'][d['gov'][line][0]]

    for c, d in specs.items():
        if 'restart' not in d:
            d['restart'] = ['[http']
        if 'date' not in d:
            d['date'] = 1
        if 'end_date' not in d:
            d['end_date'] = None
        if 'blocs' not in d:
            d['blocs'] = None
        elif d['blocs'] is not None and 'col' in d:
            set_default_colours_blocs()
        if 'gov' not in d:
            d['gov'] = None
        elif d['gov'] is not None and 'col' in d:
            set_default_colours_gov()
        if 'file_name' not in d:
            d['file_name'] = '../polling_data/' + c.lower().replace(' ', '_') + '_polling.txt'
        if 'old_data' not in d:
            path = '../polling_data/old_' + c.lower().replace(' ', '_') + '_polling.txt'
            if exists(path):
                d['old_data'] = path
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
        if 'spread' not in d:
            d['spread'] = GraphPage.spread
        if 'url' not in d:
            d['url'] = None
    return specs


def choice_setting(c):
    dat = choices[c]
    file_name = dat['file_name']
    key = dat['key']
    col = dat.get('col', None)
    blocs = dat['blocs']
    gov = dat['gov']
    start = dat.get('start', 0)
    restart = dat['restart']
    date = dat['date']
    end_date = dat['end_date']
    include = dat['include']
    vlines = dat['vlines']
    toggle_seats = dat['toggle_seats']
    zeros = dat['zeros']
    spread = dat['spread']
    return file_name, key, col, blocs, gov, start, restart, date, end_date, include, vlines, toggle_seats, zeros, spread


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
    spread = 120
    high_res = 3
    low_res = 21

    def __init__(self, choice, view='parties', metric='percentage', to_end_date=False):
        widgets.clear()

        self.graph = None
        self.choice = choice
        self.view = view
        self.metric = metric
        self.minx = -1
        self.file_name, self.key, self.col, self.blocs, self.gov, self.start, self.restart, self.date, self.end_date, \
            self.include, self.vlines, toggle_seats, self.zeros, self.spread = choice_setting(self.choice)

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
                    "../images/arrow.png")
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
                         img_path='../images/hierarchy.png')
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
                        img_path='../images/parliament.png')
        gov_button.components.append(gov_img)
        gov_button.set_tooltip('Government')
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
                          img_path='../images/ballot.png')
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
                          img_path='../images/cabinet.png')
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
                        img_path='../images/next.png')
        end_button.components.append(end_img)
        if self.end_date is None:
            end_button.disable()
        else:
            end_button.select()
        end_button.show()

        src_button = Button((screen_width - 18 / 2 * unit_size, height * 2 / 3),
                            (unit_size, unit_size), align=CENTER)
        if choices[self.choice]['url'] is None:
            src_button.disable()
        else:
            src_button.callback(functools.partial(self.open_web))
            src_button.set_tooltip('Open source data on Wikipedia')
        src_img = Image(src_button.rect.center, (src_button.rect.w * 4 / 5, src_button.rect.h * 4 / 5),
                        img_path='../images/news.png')
        src_button.components.append(src_img)
        src_button.show()

        self.spread_txt = Text(str(self.spread), (back_button.rect.centerx, back_button.rect.bottom + 8), align=TOP,
                               background_colour=BACKGROUND_COLOUR, colour=whitish if DARK_MODE else black)
        self.spread_txt.show()

        area = (self.spread_txt.rect.h, self.spread_txt.rect.h)
        self.up_spread = Button((self.spread_txt.rect.right + area[0] / 2, self.spread_txt.rect.centery), area,
                                align=LEFT)
        self.up_spread.callback(self.change_spread, returns=True)
        img = Image(self.up_spread.rect.center,
                    (self.up_spread.rect.width * 3 / 4, self.up_spread.rect.height * 3 / 4),
                    "../images/arrow.png")
        img.surface = pygame.transform.rotate(img.surface, 90)
        self.up_spread.components.append(img)
        self.up_spread.show()

        self.down_spread = Button((self.spread_txt.rect.left - area[0] / 2, self.spread_txt.rect.centery), area,
                                  align=RIGHT)
        self.down_spread.callback(self.change_spread, returns=True)
        img = Image(self.down_spread.rect.center,
                    (self.down_spread.rect.width * 3 / 4, self.down_spread.rect.height * 3 / 4),
                    "../images/arrow.png")
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

        try:
            self.change_view(view='parties')
        except:
            msg = Text("There was an error displaying the data (often caused by improperly entered/interpreted data)",
                       screen_center, background_colour=BACKGROUND_COLOUR, colour=whitish if DARK_MODE else black)
            msg.show()
            bloc_button.disable()
            seats_button.disable()
            gov_button.disable()
            self.up_spread.disable()
            self.down_spread.disable()

        remove_from_update(self.choice)

        close_button()

    def init_dat(self):
        with open(self.file_name, 'r', encoding='utf-8') as f:
            content = f.readlines()
        if 'old_data' in choices[self.choice]:
            with open(choices[self.choice]['old_data'], 'r', encoding='utf-8') as f:
                content.extend(f.readlines())
        tables = transcribe_table(content, self.key, self.choice, self.restart, self.start)
        # display_tables(tables)
        tables = process_tables(tables, self.choice, self.include, self.zeros)
        tables = filter_tables(tables, self.choice, self.include)
        tables = modify_tables(tables, self.choice, self.include, self.zeros)
        tables = interpret_tables(tables, self.include)
        return tables

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
        except ValueError:
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
        if type(relev).__name__ == "dict":
            for b, ps in relev.items():
                dat[b] = {}
                for p in ps:
                    if p in idat:
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
        else:
            for period in relev:
                start = date_kit.date_dif(today, period.start)
                if period.end is None:
                    end = None
                else:
                    end = date_kit.date_dif(today, period.end)
                for group in period.groups:
                    if group.name not in dat:
                        dat[group.name] = {}
                    for p in group.parties:
                        if p in idat:
                            for x, ys in idat[p].items():
                                if x >= start and (end is None or x <= end):
                                    if x in dat[group.name].keys():
                                        for i, y in enumerate(ys):
                                            if y is None:
                                                continue
                                            else:
                                                try:
                                                    if dat[group.name][x][i] is None:
                                                        dat[group.name][x][i] = y
                                                    else:
                                                        dat[group.name][x][i] += y
                                                except IndexError:
                                                    dat[group.name][x].append(y)
                                    else:
                                        dat[group.name][x] = ys.copy()

        return dat

    def init_graph_data(self, dat, resratio=7):
        if dat is not None and len(dat) > 0:
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
                                 dat_points=points, vlines=self.vlines, intg=intg, background_colour=BACKGROUND_COLOUR)
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

    def open_web(self):
        url = choices[self.choice]['url']
        rm = 'action=edit'
        i = url.find(rm)
        url = url[:i - 1]
        webbrowser.open(url)


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
            img_path = '../images/flags/' + entry.lower().replace(' ', '_') + '.png'
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
                img_path = '../images/exclamation.png'
                img = Image((b.rect.left, b.rect.centery), (b.rect.h * 2 / 3, b.rect.h / 2),
                            img_path, align=LEFT)
                self.notices[tag] = img
                b.components.append(img)


def get_canada_riding_data():
    try:
        with open('../misc_data/ridings.csv', 'r') as f:
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

    def failed(tag, url):
        print('Failed to load for ' + tag + ' from ' + url)

    def get_dat(dest, url, tag):
        try:
            content = urllib.request.urlopen(url)
            read_content = content.read()
            soup = BeautifulSoup(read_content, 'html.parser')
            content = soup.find_all('textarea')
            if len(content) > 0:
                text = content[0].text
            else:
                return False
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
            return True
        except urllib.error.URLError:
            return False

    def update_dat(dest, url, tag):
        success = get_dat(dest, url, tag)
        if not success:
            url2 = None
            year = choices[tag]['end_date'].year
            i = url.find(str(year))
            if i != -1:
                url2 = url[:i] + "next" + url[i + 4:]
                if i != -1:
                    success = get_dat(dest, url2, tag)
            if not success:
                failed(tag, url)
                if url2 is not None:
                    failed(tag, url2)

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
    tags = ['LPC', 'CPC', 'NDP', 'BQ', 'GPC', 'PPC', 'IND']
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
BACKGROUND_COLOUR = darkest_grey
DARK_MODE = is_dark(BACKGROUND_COLOUR)

if __name__ == '__main__':
    save_loc = '../updated.txt'
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
    surface.fill(BACKGROUND_COLOUR)

    pygame.display.set_caption('Polling')
    icon = pygame.transform.scale((pygame.image.load("../images/graph.png")), (32, 32))
    icon_surf = pygame.Surface((32, 32))
    icon_surf.fill(white)
    icon_surf.blit(icon, (0, 0), None)
    pygame.display.set_icon(icon_surf)

    run_loop(lock, background=surface, escape=False)
