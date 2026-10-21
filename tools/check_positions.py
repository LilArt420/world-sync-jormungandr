#!/usr/bin/env python3
"""Check where this mod's NPCs stand, before anyone walks there in game.

For every NPC header line in npc/**/*.txt:
  - the cell must be walkable in the client's map (.gat read from the GRFs);
  - no NPC or warp of rAthena's (the fork the app ships), of another enabled
    mod, or of World Sync Extras may stand on it or next to it (1 cell), and
    it may not sit inside a warp's trigger area.

World Sync Extras placeholders this mod replaces (same map, name, spot within
3 cells) are listed, not flagged: their navi ids go to the World Sync Extras
owner so the placeholders can be removed.

Usage: python3 -I tools/check_positions.py [--rathena DIR] [--ref REF]
                                           [--mods DIR] [--grf FILE ...]
Exit status 1 when something is flagged.
"""
import argparse
import os
import re
import struct
import subprocess
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOME = os.path.expanduser('~')
GAME = HOME + '/Documents/Games/Ragnarok Offline/Ragnarok-Portable/Ragnarok'
DEF_GRFS = [GAME + '/Game (Client)/data.grf', GAME + '/Game (kRO)/new.grf', GAME + '/Game (kRO)/data.grf']
DEF_MODS = HOME + '/Library/Application Support/Ragnarok Offline/state/mods'
MODNAME = 'world-sync-jormungandr'
# This mod's spelling -> World Sync Extras' (from the client's navigation table).
ALIASES = {'Nillem': 'Nilem'}

HEADER = re.compile(r'^([a-z0-9_@]+),(\d+),(\d+)(?:,\d+)?\t(script|warp|warp2|duplicate\([^)]*\)|shop|cashshop|itemshop|pointshop|marketshop|trader|script\(CLOAKED\))\t([^\t]+)\t?(.*)$')


class GRF:
    """Minimal GRF 0x200/0x300 reader (index + zlib entries)."""

    def __init__(self, path):
        self.f = open(path, 'rb')
        h = self.f.read(46)
        ver = struct.unpack('<I', h[42:46])[0]
        if ver == 0x300:
            off = struct.unpack('<Q', h[30:38])[0]
            self.f.seek(46 + off)
            self.f.read(4)
        else:
            off = struct.unpack('<I', h[30:34])[0]
            self.f.seek(46 + off)
        cs, us = struct.unpack('<II', self.f.read(8))
        t = zlib.decompress(self.f.read(cs))
        self.index = {}
        p = 0
        while p < len(t):
            e = t.index(b'\0', p)
            name = t[p:e].decode('cp949', 'replace').lower()
            p = e + 1
            if ver == 0x300:
                c, ca, u, fl, o = struct.unpack('<IIIBQ', t[p:p + 21])
                p += 21
            else:
                c, ca, u, fl, o = struct.unpack('<IIIBI', t[p:p + 17])
                p += 17
            self.index[name] = (ca, u, fl, o)

    def read(self, name):
        ca, u, fl, o = self.index[name.lower()]
        if fl & 6:
            return None  # DES-encrypted entry
        self.f.seek(46 + o)
        return zlib.decompress(self.f.read(ca))


class Gats:
    def __init__(self, grfs):
        self.grfs = [GRF(g) for g in grfs if os.path.exists(g)]
        self.cache = {}

    def get(self, m):
        if m not in self.cache:
            self.cache[m] = None
            for g in self.grfs:
                n = 'data\\%s.gat' % m
                if n in g.index:
                    d = g.read(n)
                    if d and d[:4] == b'GRAT':
                        w, h = struct.unpack('<ii', d[6:14])
                        self.cache[m] = (w, h, d)
                        break
        return self.cache[m]

    def walkable(self, m, x, y):
        g = self.get(m)
        if g is None:
            return None
        w, h, d = g
        if not (0 <= x < w and 0 <= y < h):
            return False
        t = struct.unpack_from('<I', d, 14 + (y * w + x) * 20 + 16)[0]
        return t not in (1, 5)


def parse(text, origin):
    out = []
    for line in text.splitlines():
        m = HEADER.match(line)
        if not m:
            continue
        mp, x, y, kind, name, rest = m.groups()
        span = (0, 0)
        sprite = ''
        if kind in ('warp', 'warp2'):
            p = rest.split(',')
            try:
                span = (int(p[0]), int(p[1]))
            except (ValueError, IndexError):
                span = (1, 1)
        else:
            sprite = rest.split(',')[0]
            sm = re.match(r'[^,]*,(\d+),(\d+),\{', rest)
            if sm:  # OnTouch area
                span = (int(sm.group(1)), int(sm.group(2)))
        out.append(dict(map=mp, x=int(x), y=int(y), kind=kind, name=name, sprite=sprite,
                        span=span, origin=origin))
    return out


def invisible(n):
    # Cloaked NPCs count as visible: they show to the players at their step.
    return n['sprite'] in ('-1', 'HIDDEN_NPC', 'HIDDEN_WARP_NPC', '111', '139', '844', 'FAKE_NPC') \
        or n['name'].startswith('#')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rathena', default=HOME + '/Projects/rathena-ep19')
    ap.add_argument('--ref', default='origin/ragnarokoffline')
    ap.add_argument('--mods', default=DEF_MODS)
    ap.add_argument('--grf', action='append')
    a = ap.parse_args()

    mine = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, 'npc')):
        for f in sorted(fn):
            if f.endswith('.txt'):
                p = os.path.join(dp, f)
                mine += parse(open(p, encoding='utf-8').read(), os.path.relpath(p, ROOT))
    maps = sorted({n['map'] for n in mine})

    others = []
    txt = subprocess.run(['git', '-C', a.rathena, 'grep', '-h', '-E', '^(' + '|'.join(re.escape(m) for m in maps) + '),[0-9]+,[0-9]+', a.ref, '--', 'npc'],
                         capture_output=True, text=True, errors='replace').stdout
    others += parse(txt, 'rathena')
    enabled = set()
    ef = os.path.join(a.mods, 'enabled.txt')
    if os.path.exists(ef):
        enabled = {l.strip() for l in open(ef) if l.strip() and not l.startswith('#')}
    for mod in sorted(os.listdir(a.mods)) if os.path.isdir(a.mods) else []:
        if mod == MODNAME or (enabled and mod not in enabled):
            continue
        nd = os.path.join(a.mods, mod, 'npc')
        for dp, dn, fn in os.walk(nd):
            for f in fn:
                if f.endswith('.txt'):
                    others += parse(open(os.path.join(dp, f), encoding='utf-8', errors='replace').read(), 'mod:' + mod)

    gats = Gats(a.grf or DEF_GRFS)
    bad = 0
    replaced = {}
    # Placeholders this mod takes over: same map and name, within 3 cells.
    for n in mine:
        base = n['name'].split('#')[0]
        base = ALIASES.get(base, base)
        for o in others:
            if o['map'] == n['map'] and o['origin'] == 'mod:world-sync-extras' and '#ws' in o['name'] \
                    and o['name'].split('#')[0] == base and max(abs(o['x'] - n['x']), abs(o['y'] - n['y'])) <= 3:
                replaced.setdefault(o['name'].split('#ws')[1], (o, n))
    gone = {id(o) for o, n in replaced.values()}
    others = [o for o in others if id(o) not in gone]
    for n in mine:
        w = gats.walkable(n['map'], n['x'], n['y'])
        if w is False and not invisible(n):
            # An NPC may stand on a wall or a cliff edge as long as a player
            # can reach a cell next to it to click it.
            if not any(gats.walkable(n['map'], n['x'] + dx, n['y'] + dy)
                       for dx in range(-2, 3) for dy in range(-2, 3)):
                print('UNREACHABLE   %(map)s,%(x)d,%(y)d %(name)s (%(origin)s)' % n)
                bad += 1
        elif w is None:
            print('no .gat for %(map)s (%(name)s)' % n)
        base = n['name'].split('#')[0]
        for o in others:
            if o['map'] != n['map']:
                continue
            dx, dy = abs(o['x'] - n['x']), abs(o['y'] - n['y'])
            if o['kind'] in ('warp', 'warp2') or (invisible(o) and o['span'] != (0, 0)):
                if dx <= o['span'][0] and dy <= o['span'][1] and not invisible(n):
                    print('IN TRIGGER    %s,%d,%d %s  <- %s %s,%d,%d span %s (%s)' % (n['map'], n['x'], n['y'], n['name'], o['kind'], o['name'], o['x'], o['y'], o['span'], o['origin']))
                    bad += 1
                continue
            if invisible(o) or invisible(n):
                continue
            if max(dx, dy) <= 1:
                print('TOO CLOSE     %s,%d,%d %s  <- %s,%d,%d %s (%s)' % (n['map'], n['x'], n['y'], n['name'], o['map'], o['x'], o['y'], o['name'], o['origin']))
                bad += 1
    print('\n%d NPC lines checked on %d maps; %d problems.' % (len(mine), len(maps), bad))
    if replaced:
        ids = sorted(replaced, key=int)
        print('Replaces %d World Sync Extras placeholders: %s' % (len(ids), ' '.join(ids)))
        with open(os.path.join(ROOT, 'tools', 'replaced_placeholders.txt'), 'w') as f:
            for i in ids:
                o, n = replaced[i]
                f.write('%s\t%s,%d,%d\t%s\t%s\n' % (i, o['map'], o['x'], o['y'], o['name'], n['name']))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
