#!/usr/bin/env python3
"""Cross-check F_WSJ_Scenes against the NPCs: every name in the table must be
an NPC of this mod, and every CLOAKED NPC must be in the table (or it never
shows). Also lists quest ids the scripts use that db/quest_db.yml lacks."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
txt = {f: open(f).read() for f in glob.glob(os.path.join(ROOT, 'npc', '*.txt'))}
allt = '\n'.join(txt.values())
npcs = {}
for m in re.finditer(r'^[a-z0-9_@]+,\d+,\d+,\d+\t(script\(CLOAKED\)|script|duplicate\([^)]*\))\t([^\t]+)\t', allt, re.M):
    npcs[m.group(2)] = m.group(1)
common = txt[os.path.join(ROOT, 'npc', 'ep20_common.txt')]
table = set(re.findall(r'"([^"]+#wsj[^"]*)","-?\d+","\d+"', common))
table |= {"Nyar's Clone#wsj%d" % i for i in range(1, 13)}
bad = 0
for n in sorted(table):
    if n not in npcs:
        print('in table, no such NPC:', n); bad += 1
for n, k in sorted(npcs.items()):
    if 'CLOAKED' in k and n not in table:
        print('cloaked but never shown:', n); bad += 1
used = set(int(x) for x in re.findall(r'(?:setquest|completequest|checkquest\(|isbegin_quest\()\s*(\d{4,5})', allt))
for s in re.findall(r'F_WSJ_Step", \d+, "([\d,]*)", "([\d,]*)"', allt):
    for part in s:
        used |= {int(x) for x in part.split(',') if x}
for s in re.findall(r'setarray \.@q, ([\d, ]+);', allt):
    used |= {int(x) for x in s.split(',')}
db = set(int(x) for x in re.findall(r'^  - Id: (\d+)', open(os.path.join(ROOT, 'db', 'quest_db.yml')).read(), re.M))
for q in sorted(used - db):
    print('quest used but not in db/quest_db.yml:', q); bad += 1
for q in sorted(db - used):
    print('quest in db but unused:', q)
print('%d NPCs, %d in scene table, %d quests used; %d problems' % (len(npcs), len(table), len(used), bad))
sys.exit(1 if bad else 0)
