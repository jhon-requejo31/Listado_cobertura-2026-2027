#!/usr/bin/env python3
"""Genera cobertura.js (periodo 2026-II) desde cobertura_2026-II.xlsx.  Uso: python build_cobertura.py cobertura_2026-II.xlsx cobertura.js"""
import sys, json, pandas as pd
d = pd.read_excel(sys.argv[1], dtype=str).fillna('')
d['u'] = pd.to_numeric(d['usuario_pob_obj'], errors='coerce').fillna(0)
d['b'] = (d['Cobertura'].str.strip().str.lower() != 'cobertura').astype(int)  # 0 cobertura, 1 brecha
g = d.groupby([d['UNIDAD TERRITORIAL'].str.strip().str.upper(), d['DEPARTAMENTO'].str.strip().str.upper(), d['NIVEL EDUCATIVO'].str.strip().str.upper(), 'b']).agg(n=('u', 'size'), u=('u', 'sum')).reset_index()
rows = [[r.iloc[0], r.iloc[1], r.iloc[2], int(r.b), int(r.n), int(r.u)] for _, r in g.iterrows()]
open(sys.argv[2], 'w', encoding='utf8').write('window.COBERTURA={periodo:"2026-II",rows:' + json.dumps(rows, ensure_ascii=False, separators=(',', ':')) + '};')
print(len(rows), 'filas; cobertura', d[d.b == 0].shape[0], 'brecha', d[d.b == 1].shape[0])
print(d.groupby(d['UNIDAD TERRITORIAL'].str.upper()).apply(lambda x: (x.b.eq(0).sum(), int(x.u[x.b.eq(0)].sum()))).head(6))
