#!/usr/bin/env python3
"""Can a player walk (or be carried) to every map this mod uses?

Builds the map graph from what the server loads by default:
  - rAthena's scripts at the app's pinned commit (warps, and NPCs that
    `warp` the player somewhere),
  - every enabled mod in state/mods, with npc/when/<key>/ folders only for
    settings that are on (state/mod-settings.json, else the default),
  - this mod's own scripts,
then walks it from the Episode 19 hubs (Frozen Tail, Ice Castle) and lists
every map in npc/ or in the quest log's <NAVI> links that can't be reached.
Memorial dungeons (1@...) are entered through instance NPCs, so they're
listed apart.

Usage: python3 -I tools/check_reach.py [--ref COMMIT]
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOME = os.path.expanduser('~')
STATE = HOME + '/Library/Application Support/Ragnarok Offline/state'
MODNAME = 'world-sync-jormungandr'
START = ['icecastle', 'jor_tail', 'icas_in']

HDR = re.compile(r'^([a-z0-9_@]+),\d+,\d+,\d+\t(warp|warp2|script|script\(CLOAKED\))\t[^\t]+\t(.*)$')
WARP_DEST = re.compile(r'\d+,\d+,([a-z0-9_@]+),\d+,\d+')
SCRIPT_WARP = re.compile(r'\bwarp\s*\(?\s*"([a-z0-9_@]+)"')


def links(text, out, origin):
    cur = None
    for line in text.splitlines():
        m = HDR.match(line)
        if m:
            src, kind, rest = m.groups()
            cur = src if kind.startswith('script') else None
            if kind in ('warp', 'warp2'):
                d = WARP_DEST.match(rest)
                if d:
                    out.setdefault(src, set()).add((d.group(1), origin))
            continue
        if line.startswith('}'):
            cur = None
        if cur:
            for d in SCRIPT_WARP.findall(line):
                out.setdefault(cur, set()).add((d, origin))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rathena', default=HOME + '/Projects/rathena-ep19')
    ap.add_argument('--ref', default='2b26d2936')
    a = ap.parse_args()
    graph = {}
    files = subprocess.run(['git', '-C', a.rathena, 'grep', '-l', '-E', r'warp', a.ref, '--', 'npc'],
                           capture_output=True, text=True).stdout.split()
    for f in files:
        txt = subprocess.run(['git', '-C', a.rathena, 'show', f], capture_output=True, text=True, errors='replace').stdout
        links(txt, graph, 'rathena')
    enabled = set()
    ef = os.path.join(STATE, 'mods', 'enabled.txt')
    if os.path.exists(ef):
        enabled = {l.strip() for l in open(ef) if l.strip() and not l.startswith('#')}
    settings = {}
    sf = os.path.join(STATE, 'mod-settings.json')
    if os.path.exists(sf):
        settings = json.load(open(sf))
    for mod in sorted(os.listdir(os.path.join(STATE, 'mods'))):
        md = os.path.join(STATE, 'mods', mod)
        if mod == MODNAME or not os.path.isdir(md) or (enabled and mod not in enabled):
            continue
        defaults = {}
        try:
            for s in json.load(open(os.path.join(md, 'mod.json'))).get('settings', []):
                defaults[s['key']] = s.get('default')
        except (OSError, ValueError):
            pass
        on = dict(defaults)
        on.update(settings.get(mod, {}) if isinstance(settings.get(mod), dict) else {})
        for dp, dn, fn in os.walk(os.path.join(md, 'npc')):
            rel = os.path.relpath(dp, os.path.join(md, 'npc')).split(os.sep)
            if rel[0] == 'when' and len(rel) > 1 and not on.get(rel[1]):
                continue
            for f in fn:
                if f.endswith('.txt'):
                    links(open(os.path.join(dp, f), errors='replace').read(), graph, 'mod:' + mod)
    mine = ''
    for dp, dn, fn in os.walk(os.path.join(ROOT, 'npc')):
        for f in fn:
            if f.endswith('.txt'):
                mine += open(os.path.join(dp, f)).read() + '\n'
    links(mine, graph, 'this mod')

    seen = set(START)
    todo = list(START)
    while todo:
        m = todo.pop()
        for d, o in graph.get(m, ()):
            if d not in seen:
                seen.add(d)
                todo.append(d)
    used = set(re.findall(r'^([a-z0-9_@]+),\d+,\d+,\d+\t', mine, re.M))
    lub = os.path.join(ROOT, 'System', 'OngoingQuestInfoList.lub')
    if os.path.exists(lub):
        used |= set(re.findall(r'<INFO>([a-z0-9_@]+)(?:\.gat)?,', open(lub).read()))
    bad = sorted(m for m in used if m not in seen and not m.startswith('1@'))
    md = sorted(m for m in used if m.startswith('1@'))
    for m in bad:
        into = sorted({(s, o) for s, ds in graph.items() for d, o in ds if d == m})
        print('UNREACHABLE %-12s links in: %s' % (m, ', '.join('%s (%s)' % x for x in into) or 'none'))
    print('%d maps used, %d reachable from %s; memorial dungeons: %s' % (len(used), len(used) - len(bad), '/'.join(START), ' '.join(md)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
