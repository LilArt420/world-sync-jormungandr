#!/usr/bin/env python3
"""Print the cells around map,x,y: '.' walkable, '#' blocked, 'N' an NPC
(rAthena or enabled mods), 'o' this mod, '@' the centre.
Usage: python3 -I tools/near.py <map> <x> <y> [radius]"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_positions as cp

m, x, y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
r = int(sys.argv[4]) if len(sys.argv) > 4 else 6
g = cp.Gats(cp.DEF_GRFS)
txt = subprocess.run(['git', '-C', cp.HOME + '/Projects/rathena-ep19', 'grep', '-h', '-E', '^' + m + ',[0-9]+,[0-9]+', 'origin/ragnarokoffline', '--', 'npc'], capture_output=True, text=True, errors='replace').stdout
others = cp.parse(txt, 'r')
for mod in os.listdir(cp.DEF_MODS):
    nd = os.path.join(cp.DEF_MODS, mod, 'npc')
    if mod == cp.MODNAME: continue
    for dp, dn, fn in os.walk(nd):
        for f in fn:
            if f.endswith('.txt'):
                others += cp.parse(open(os.path.join(dp, f), errors='replace').read(), mod)
mine = []
for dp, dn, fn in os.walk(os.path.join(cp.ROOT, 'npc')):
    for f in fn:
        if f.endswith('.txt'):
            mine += cp.parse(open(os.path.join(dp, f)).read(), 'me')
occ = {(o['x'], o['y']): 'N' for o in others if o['map'] == m and not cp.invisible(o) and o['kind'] not in ('warp', 'warp2')}
for o in others:
    if o['map'] == m and o['kind'] in ('warp', 'warp2'):
        occ[(o['x'], o['y'])] = 'W'
occ.update({(o['x'], o['y']): 'o' for o in mine if o['map'] == m and not cp.invisible(o)})
for yy in range(y + r, y - r - 1, -1):
    row = ''
    for xx in range(x - r, x + r + 1):
        c = occ.get((xx, yy))
        if (xx, yy) == (x, y): c = '@'
        if not c:
            w = g.walkable(m, xx, yy)
            c = '.' if w else '#'
        row += c
    print('%4d %s' % (yy, row))
print('     x from %d to %d' % (x - r, x + r))
