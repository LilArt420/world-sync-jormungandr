#!/usr/bin/env python3
"""Generate db/quest_db.yml and System/OngoingQuestInfoList.lub for the
quests the scripts use.

Titles, summaries and descriptions come from the client's English quest
table (ROenglishRE's translation of kRO, free to use and modify), with the
names made to match the NPCs the player meets (Lazy, not Leize; Rgan, not
Lergan...). Kill targets are this mod's: the client table has none.

Usage: python3 -I tools/gen_quests.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOME = os.path.expanduser('~')
GAME = HOME + '/Documents/Games/Ragnarok Offline/Ragnarok-Portable/Ragnarok'
EN = GAME + '/Game (kRO)/SystemEN/OngoingQuests.lub'
sys.path.insert(0, HOME + '/Projects/rathena-ep19/tools/regional_items')
from luadata import load_any  # noqa: E402
sys.path.insert(0, HERE)
from ep21_quests import EP21  # noqa: E402

# Quests used by npc/, in story order.
QUESTS = (list(range(16691, 16705)) + list(range(17690, 17710)) + list(range(17712, 17717)) + [17719]
          + [8839, 8840, 8841, 8842, 8843, 8846, 8847, 8848, 8849, 8850, 8851, 8854]
          + list(range(23100, 23110)) + list(range(23112, 23119)) + list(range(18220, 18234))
          # dailies
          + [17710, 17711, 17717, 17718, 8844, 8845, 18234, 18235, 18236, 18237, 18238, 18239, 23110, 23111]
          # Episode 21
          + [18334, 18335, 18336, 18337, 23240, 23241, 23242, 23243] + list(range(24000, 24019))
          + list(range(23244, 23256)) + list(range(8882, 8895))
          + list(range(17752, 17770)) + list(range(18338, 18362)) + [8914, 8915, 8916, 12647, 12656]
          # after the stories: EP20 extras, EP21 Alberta/ghost ship, side stories, dailies
          + [8852, 8853, 12588, 12590, 12591] + list(range(16802, 16827))
          + list(range(17770, 17790)) + list(range(19184, 19204)) + [23256, 23257] + list(range(24019, 24049)))

# Kill counters (the client's text names the monsters, not the numbers).
TARGETS = {
    17693: ['      - Mob: EP20_RGAN_WARLOCK', '        Count: 5'],
    17703: ['      - Id: 1', '        Count: 3', '        MapName: Serpent\'s Maze parasites', '        Location: jor_maze',
            '        MapMobTargets:', '          EP20_JORMUNGUARD1: true', '          EP20_JORMUNGUARD2: true',
            '          EP20_JORGAN_GUARDIAN: true'],
    23101: ['      - Mob: EP19_ICE_GANGU', '        Count: 5'],
    23102: ['      - Mob: EP19_SHINING_SEAWEED', '        Count: 5'],
    23109: ['      - Mob: EP20_JORGAN_WARLOCK', '        Count: 5'],
    17710: ['      - Mob: EP20_JORMUNGUARD1', '        Count: 10', '      - Mob: EP20_JORMUNGUARD2', '        Count: 10'],
    23111: ['      - Mob: EP20_JORGAN_WARLOCK', '        Count: 15'],
    17777: ['      - Id: 1', '        Count: 300', "        MapName: North of the Raised Land", '        Location: jor_raise1'],
    17778: ['      - Id: 1', '        Count: 300', "        MapName: South of the Raised Land", '        Location: jor_raise2'],
    17782: ['    Drops:', '      - Mob: EP21_YORMI_B', '        Item: aegis_1001629', '        Count: 1', '        Rate: 2500'],
    17783: ['    Drops:', '      - Mob: EP21_ICESEAHORSE', '        Item: aegis_1001648', '        Count: 1', '        Rate: 2500'],
    17784: ['    Drops:', '      - Mob: EP21_YORTUS_B', '        Item: aegis_1001639', '        Count: 1', '        Rate: 2500'],
    17785: ['    Drops:', '      - Mob: EP21_YORDOS_C', '        Item: aegis_1001637', '        Count: 1', '        Rate: 2500'],
    17786: ['    Drops:', '      - Mob: EP21_CLIOLIMA', '        Item: aegis_1001646', '        Count: 1', '        Rate: 2500'],
    17787: ['    Drops:', '      - Mob: EP21_SEAWIND', '        Item: aegis_1001642', '        Count: 1', '        Rate: 2500'],
    17788: ['    Drops:', '      - Mob: EP21_LETTERSTER', '        Item: aegis_1001645', '        Count: 1', '        Rate: 2500'],
    23256: ['    Drops:', '      - Mob: EP21_SKIPSKIPPER', '        Item: aegis_1001641', '        Count: 1', '        Rate: 1000'],
    24031: ['    Drops:', '      - Mob: EP21_ROCKSTRIKER', '        Item: aegis_1001647', '        Count: 1', '        Rate: 2500', '      - Mob: EP21_SKIPSKIPPER', '        Item: aegis_1001644', '        Count: 1', '        Rate: 2500'],
    24033: ['      - Mob: EP21_SCALLEG', '        Count: 50'],
    24035: ['      - Mob: EP21_VELELLING', '        Count: 50'],
    24037: ['      - Id: 1', '        Count: 100', "        MapName: Gimle 1F", '        Location: jor_tmple1'],
    24039: ['      - Id: 1', '        Count: 100', "        MapName: Gimle 2F", '        Location: jor_tmple2'],
    24042: ['      - Id: 1', '        Count: 300', "        MapName: Yorskalf 1F", '        Location: jor_sklf1'],
    24044: ['      - Id: 1', '        Count: 1500', "        MapName: Yorskalf 1F", '        Location: jor_sklf1'],
    24046: ['      - Id: 1', '        Count: 300', "        MapName: Yorskalf 2F", '        Location: jor_sklf2'],
    24048: ['      - Id: 1', '        Count: 1500', "        MapName: Yorskalf 2F", '        Location: jor_sklf2'],
    23247: ['      - Mob: EP21_SKIPSKIPPER', '        Count: 10',
            '    Drops:', '      - Mob: EP21_SKIPSKIPPER', '        Item: aegis_1001641', '        Count: 1', '        Rate: 1000'],
    18234: ['      - Id: 1', '        Count: 30', '        MapName: Deep Roots Cave', '        Location: jor_root3'],
    18236: ['      - Id: 1', '        Count: 30', '        MapName: Roots 1st floor Rgans', '        Location: jor_root1',
            '        MapMobTargets:', '          EP20_RGAN_WARLOCK: true', '          EP20_RGAN_HEALER: true'],
    18238: ['      - Id: 1', '        Count: 30', '        MapName: Roots 2nd floor Rgans', '        Location: jor_root2',
            '        MapMobTargets:', '          EP20_JORGAN_WARLOCK: true', '          EP20_JORGAN_HEALER: true'],
}

# Standby quests: the daily reset.
STANDBY = {17711, 17717, 8844, 18235, 18237, 18239, 23110, 12647, 8852, 12588, 16823, 17779, 17780, 17789,
           19185, 19197, 19199, 23257, 24030, 24032, 24034, 24036, 24038, 24040, 24043, 24047}
WEEKLY = {24045}

# Summaries that should say how many.
SUMMARY = {
    17693: 'Defeat 5 Superior Rgan Warlocks',
    17703: 'Defeat 3 parasites in the Serpent\'s Maze',
    23101: '5 Ice Gangus, 3 Frozen Insect Shells',
    23102: '5 Shining Seaweeds, 3 Shiny Seaweed Stems',
    18234: 'Defeat 30 monsters in the Deep Roots Cave',
    18236: 'Defeat 30 Rgans on the Roots 1st floor',
    18238: 'Defeat 30 Rgans on the Roots 2nd floor',
    23111: 'Defeat 15 Jormun Warlocks',
}

# Client spelling -> the name the NPC has in game (longest first).
NAMES = [
    ('Gamiravagandha', 'Gamirabagand'), ('Numkasaigargand', 'Numkasaigagand'),
    ('Onnacharamelgand', 'Onnaecheramelgand'), ('Jagdagumigand', 'Jakreudagumigand'),
    ('Clejainamogand', 'Kljeinamogand'), ('Nasioramigand', 'Nalsioramigand'),
    ('Halseybygand', 'Holsibigand'), ('Pamoshgand', 'Pamoshugand'), ('Pamosugand', 'Pamoshugand'), ('Eryligand', 'Eririgand'),
    ('Sarekgandh', 'Sarekgand'), ('Saergand', 'Sarekgand'), ('Saregand', 'Sarekgand'),
    ('Lasgand', 'Rasgand'), ('Lergans', 'Rgans'), ('Lergan', 'Rgan'), ('Lecans', 'Rgans'),
    ('Legan', 'Rgan'), ("Le'gan", 'Rgan'), ('Lehrar', 'Lehar'), ('Leize', 'Lazy'),
    ('Boclinde', 'Voglinde'), ('Velgund', 'Vellgunde'), ('Bagoth', 'Bagot'),
    ('Horror', 'Horuru'), ('Horr', 'Horuru'), ('Talk to Rage', 'Talk to Lazy'),
    ('Kokoro', 'Kororo'), ('Orelli', 'Aurelie'), ('Aureli', 'Aurelie'), ('Aureliee', 'Aurelie'),
    ('Leo and', 'Leon and'), ('to Leo', 'to Leon'), ('Lord Naya', 'Lord Nyar'),
    ('Diving Awin', 'Diving Iwin'), ('Awin', 'Iwin'), ('Icesen', 'the Ice Castle'),
    ('Ice Angoos', 'Ice Gangus'), ('Snake Roots', 'Roots of the Serpent God'), ('Yormungand', 'Jormungandr'), ('Icy Zone', 'Frozen Zone'),
    ('Icegard', 'Issgard'), ('Triss', 'Tris'), ('Nilem', 'Nillem'), ('Ephesus Walter Megas', 'Epesto Walter Megas'),
    ('Hunter Sanguine', 'Hunter Sanguin'), ('Lalira Wigner', 'Lalaira Wigner'), ('Laraira', 'Lalaira'),
    ('loss of Eiji', 'lost mind'), ('prt_elib,60,37', 'jor_twig,113,146'), ('Lara told', 'Lalaira told'),
]


def fix(s):
    for a, b in NAMES:
        s = s.replace(a, b)
    s = s.replace('the the ', 'the ').replace('The the ', 'The ')
    s = s.replace('Aurelieee', 'Aurelie').replace('Aurelie e', 'Aurelie')
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\t', '').replace('\r', '')
    s = s.encode('ascii', 'ignore').decode()
    return s


def lua(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


def main():
    q = load_any(EN, 'utf-8')['QuestInfoList']
    yml = ['# World Sync: Jormungandr - quests of Episode 20 (The Undying One).',
           '# Generated by tools/gen_quests.py. Titles from the client\'s quest table.',
           'Header:', '  Type: QUEST_DB', '  Version: 3', '', 'Body:']
    lub = ['-- World Sync: Jormungandr: quest log text for Episode 20.',
           '-- From the kRO client\'s quest table as translated by ROenglishRE',
           '-- (https://github.com/llchrisll/ROenglishRE, free to use and modify),',
           '-- with names matching the NPCs in game. Generated by tools/gen_quests.py.',
           'QuestInfoList = {']
    for i in QUESTS:
        if i in EP21:
            t, sm, ds = EP21[i]
            e = {'Title': t, 'Summary': sm, 'Description': [ds]}
        else:
            e = q[i]
        title = fix(e['Title'])
        d = e.get('Description') or {}
        if isinstance(d, dict):
            d = [d[k] for k in sorted(d)]
        desc = fix(' '.join(x.strip() for x in d))
        summ = SUMMARY.get(i, fix(e.get('Summary') or ''))
        if i in EP21:
            title, desc, summ = EP21[i][0], EP21[i][2], EP21[i][1]
        yml.append('  - Id: %d' % i)
        yml.append('    Title: "%s"' % title.replace('"', "'"))
        if i in STANDBY:
            yml.append('    TimeLimit: 4h')
        if i in WEEKLY:
            yml.append('    TimeLimit: Friday 4h')
        if i in TARGETS:
            t = TARGETS[i]
            if not t[0].startswith('    Drops:'):
                yml.append('    Targets:')
            yml += t
        lub.append('\t[%d] = {' % i)
        lub.append('\t\tTitle = %s,' % lua(title))
        lub.append('\t\tIconName = "%s",' % ('ico_dq.bmp' if ('Standby' in title or i in STANDBY or i == 12656) else 'ico_ep.bmp'))
        lub.append('\t\tDescription = { %s },' % lua(desc))
        lub.append('\t\tSummary = %s' % lua(summ))
        lub.append('\t},')
    lub.append('}')
    os.makedirs(os.path.join(ROOT, 'db'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'System'), exist_ok=True)
    open(os.path.join(ROOT, 'db', 'quest_db.yml'), 'w').write('\n'.join(yml) + '\n')
    open(os.path.join(ROOT, 'System', 'OngoingQuestInfoList.lub'), 'w', encoding='ascii').write('\n'.join(lub) + '\n')
    print('%d quests' % len(QUESTS))


if __name__ == '__main__':
    main()
