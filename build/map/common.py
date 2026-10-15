"""Shared helpers for the PPS map v2 build (reads the original page, never writes it)."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(KIT, 'pages', 'pps-walk-redraw.html')
OUT = os.path.join(KIT, 'pages', 'pps-walk-redraw-v2.html')
WORK = os.path.join(HERE, 'work')
os.makedirs(WORK, exist_ok=True)
X0, Y0 = 1229300, 454300
LAT_M = 111320.0      # metres per degree latitude
KX = 0.5 ** 0 * __import__('math').cos(__import__('math').radians(45.54))

def grab(t, pre, post):
    i = t.index(pre) + len(pre)
    return t[i:t.index(post, i)]

def load_page():
    return open(SRC, encoding='utf-8').read()

def dec(s):
    """page polygon/line encoding -> list of rings of (lon, lat)"""
    out = []
    for rr in s.split('|'):
        X = Y = 0; ring = []
        for i, p in enumerate(rr.strip().split(' ')):
            a, b = map(int, p.split(','))
            if i == 0: X, Y = a, b
            else: X += a; Y += b
            ring.append(((X - X0) / 1e4, (Y + Y0) / 1e4))
        out.append(ring)
    return out

def enc_ring(ring):
    pts = [(round(x * 1e4 + X0), round(y * 1e4 - Y0)) for x, y in ring]
    # drop consecutive duplicates
    q = [pts[0]]
    for p in pts[1:]:
        if p != q[-1]: q.append(p)
    if len(q) < 3: return None
    s = '%d,%d' % q[0]
    for a, b in zip(q, q[1:]):
        s += ' %d,%d' % (b[0] - a[0], b[1] - a[1])
    return s
