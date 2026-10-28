#!/usr/bin/env python3
"""
Generatore Blueprint Professionale DXF per Cabinato Arcade Bartop 2P
Configurazione CLASSIC CABARET (Top Accorciato a ~150mm - Tagli 100% a 90°):
- Silhouette Classica Cabaret: Schienale superiore inclinato in avanti a ~150mm dal frontale,
  tetto compatto (142mm), zero ingombro sporgente sul retro.
- Incasso Monitor 21.5" e Plancia Comandi completamente protetti all'interno delle fiancate.
- Tagli al 100% a 90°: Nessun taglio obliquo/miter, tutti i pannelli squadrati a 90°.
- Nastro T-Molding perimetrale 2.0 mm su entrambi i bordi delle guance.
- Zero Collisioni e Zero Gap: Contatto continuo perfetto tra tutti i pannelli.
"""

import math
import sys

class DxfWriter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.entities = []

    def add_line(self, p1, p2, layer="0", color=7):
        self.entities.append({
            'type': 'LINE',
            'layer': layer,
            'color': color,
            'p1': p1,
            'p2': p2
        })

    def add_circle(self, center, radius, layer="0", color=7):
        self.entities.append({
            'type': 'CIRCLE',
            'layer': layer,
            'color': color,
            'center': center,
            'radius': radius
        })

    def add_polyline(self, points, closed=True, layer="0", color=7):
        self.entities.append({
            'type': 'LWPOLYLINE',
            'layer': layer,
            'color': color,
            'points': points,
            'closed': closed
        })

    def add_rect(self, p1, p2, fillet=0, layer="0", color=7):
        x1, y1 = p1
        x2, y2 = p2
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        if fillet <= 0:
            pts = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
            self.add_polyline(pts, closed=True, layer=layer, color=color)
        else:
            r = min(fillet, (xmax - xmin)/2, (ymax - ymin)/2)
            pts = []
            pts.append([xmin + r, ymin])
            pts.append([xmax - r, ymin])
            for a in [15, 30, 45, 60, 75, 90]:
                rad = math.radians(270 + a)
                pts.append([round(xmax - r + r*math.cos(rad), 2), round(ymin + r + r*math.sin(rad), 2)])
            pts.append([xmax, ymax - r])
            for a in [15, 30, 45, 60, 75, 90]:
                rad = math.radians(0 + a)
                pts.append([round(xmax - r + r*math.cos(rad), 2), round(ymax - r + r*math.sin(rad), 2)])
            pts.append([xmin + r, ymax])
            for a in [15, 30, 45, 60, 75, 90]:
                rad = math.radians(90 + a)
                pts.append([round(xmin + r + r*math.cos(rad), 2), round(ymax - r + r*math.sin(rad), 2)])
            pts.append([xmin, ymin + r])
            for a in [15, 30, 45, 60, 75, 90]:
                rad = math.radians(180 + a)
                pts.append([round(xmin + r + r*math.cos(rad), 2), round(ymin + r + r*math.sin(rad), 2)])
            self.add_polyline(pts, closed=True, layer=layer, color=color)

    def add_slot(self, p1, p2, width, layer="0", color=7):
        x1, y1 = p1
        x2, y2 = p2
        r = width / 2.0
        if abs(y1 - y2) < 1e-4:
            xmin = min(x1, x2)
            xmax = max(x1, x2)
            yc = y1
            pts = []
            pts.append([xmin, yc - r])
            pts.append([xmax, yc - r])
            for a in range(-90, 91, 15):
                rad = math.radians(a)
                pts.append([round(xmax + r*math.cos(rad), 2), round(yc + r*math.sin(rad), 2)])
            pts.append([xmax, yc + r])
            pts.append([xmin, yc + r])
            for a in range(90, 271, 15):
                rad = math.radians(a)
                pts.append([round(xmin + r*math.cos(rad), 2), round(yc + r*math.sin(rad), 2)])
            self.add_polyline(pts, closed=True, layer=layer, color=color)
        else:
            dx = x2 - x1
            dy = y2 - y1
            L = math.hypot(dx, dy)
            ux, uy = dx/L, dy/L
            nx, ny = -uy, ux
            pts = []
            pts.append([round(x1 + r*nx, 2), round(y1 + r*ny, 2)])
            pts.append([round(x2 + r*nx, 2), round(y2 + r*ny, 2)])
            for a in range(-90, 91, 15):
                rad = math.radians(a)
                vx = ux*math.sin(rad) + nx*math.cos(rad)
                vy = uy*math.sin(rad) + ny*math.cos(rad)
                pts.append([round(x2 + r*vx, 2), round(y2 + r*vy, 2)])
            pts.append([round(x2 - r*nx, 2), round(y2 - r*ny, 2)])
            pts.append([round(x1 - r*nx, 2), round(y1 - r*ny, 2)])
            for a in range(90, 271, 15):
                rad = math.radians(a)
                vx = ux*math.sin(rad) + nx*math.cos(rad)
                vy = uy*math.sin(rad) + ny*math.cos(rad)
                pts.append([round(x1 + r*vx, 2), round(y1 + r*vy, 2)])
            self.add_polyline(pts, closed=True, layer=layer, color=color)

    def add_text(self, at, text, height=12, justify="L", layer="0", color=7):
        self.entities.append({
            'type': 'TEXT',
            'layer': layer,
            'color': color,
            'at': at,
            'text': text,
            'height': height,
            'justify': justify
        })

    def save(self):
        lines = [
            "0", "SECTION",
            "2", "HEADER",
            "9", "$ACADVER",
            "1", "AC1015",
            "0", "ENDSEC",
            "0", "SECTION",
            "2", "TABLES",
            "0", "TABLE",
            "2", "LAYER",
            "70", "5",
            "0", "LAYER", "2", "0", "70", "0", "62", "7", "6", "CONTINUOUS",
            "0", "LAYER", "2", "CUT", "70", "0", "62", "7", "6", "CONTINUOUS",
            "0", "LAYER", "2", "GUIDE", "70", "0", "62", "1", "6", "DASHED",
            "0", "LAYER", "2", "TEXT", "70", "0", "62", "2", "6", "CONTINUOUS",
            "0", "LAYER", "2", "TMOLDING", "70", "0", "62", "4", "6", "CONTINUOUS",
            "0", "ENDTAB",
            "0", "ENDSEC",
            "0", "SECTION",
            "2", "ENTITIES"
        ]

        for ent in self.entities:
            t = ent['type']
            layer = ent.get('layer', '0')
            color = ent.get('color', 7)

            if t == 'LINE':
                p1 = ent['p1']
                p2 = ent['p2']
                lines += [
                    "0", "LINE",
                    "8", layer,
                    "62", str(color),
                    "10", f"{p1[0]:.3f}",
                    "20", f"{p1[1]:.3f}",
                    "30", "0.0",
                    "11", f"{p2[0]:.3f}",
                    "21", f"{p2[1]:.3f}",
                    "31", "0.0"
                ]

            elif t == 'CIRCLE':
                c = ent['center']
                r = ent['radius']
                lines += [
                    "0", "CIRCLE",
                    "8", layer,
                    "62", str(color),
                    "10", f"{c[0]:.3f}",
                    "20", f"{c[1]:.3f}",
                    "30", "0.0",
                    "40", f"{r:.3f}"
                ]

            elif t == 'LWPOLYLINE':
                pts = ent['points']
                closed = ent['closed']
                lines += [
                    "0", "POLYLINE",
                    "8", layer,
                    "62", str(color),
                    "66", "1",
                    "70", "1" if closed else "0",
                    "10", "0.0",
                    "20", "0.0",
                    "30", "0.0"
                ]
                for p in pts:
                    lines += [
                        "0", "VERTEX",
                        "8", layer,
                        "10", f"{p[0]:.3f}",
                        "20", f"{p[1]:.3f}",
                        "30", "0.0"
                    ]
                lines += [
                    "0", "SEQEND",
                    "8", layer
                ]

            elif t == 'TEXT':
                at = ent['at']
                txt = ent['text']
                h = ent['height']
                just = ent.get('justify', 'L')
                lines += [
                    "0", "TEXT",
                    "8", layer,
                    "62", str(color),
                    "10", f"{at[0]:.3f}",
                    "20", f"{at[1]:.3f}",
                    "30", "0.0",
                    "40", f"{h:.3f}",
                    "1", txt
                ]
                if just == 'C':
                    lines += [
                        "72", "1",
                        "11", f"{at[0]:.3f}",
                        "21", f"{at[1]:.3f}",
                        "31", "0.0"
                    ]
                elif just == 'R':
                    lines += [
                        "72", "2",
                        "11", f"{at[0]:.3f}",
                        "21", f"{at[1]:.3f}",
                        "31", "0.0"
                    ]

        lines += [
            "0", "ENDSEC",
            "0", "EOF"
        ]

        with open(self.filepath, 'w') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"DXF generato con successo: {self.filepath} ({len(self.entities)} entità)")


def build_cabinet_lep1_project(filepath="/home/paolo/Projects/cabinato/cabinato_arcade_cadcraft.dxf"):
    dxf = DxfWriter(filepath)

    w_int = 514.0       # Larghezza interna netta per schermo AOC 500mm (+14mm tolleranza)
    th_slot = 19.2      # Larghezza asola mortasa per legno MDF 19mm (+0.2mm tolleranza)
    tenon_len = 15.0    # Sporgenza tenone maschio

    # =========================================================================
    # COLONNA 1: FIANCATA LATERALE (SX/DX) - (X = 0 .. 485, Y = 0 .. 602)
    # CONFIGURAZIONE CLASSIC CABARET (TETTO ~150mm, SCHIENALE SPIOVENTE)
    # =========================================================================
    print("1. Fiancata Laterale Classic Cabaret (12 Mortase Verificate, Tagli 90°)...")

    # Silhouette esterna Classic Cabaret (28 punti)
    side_poly = [
        [0.0, 0.0],
        [410.0, 0.0],        # Base appoggio 410mm
        [430.0, 15.0],       # Raccordo inferiore
        [455.0, 75.0],       # Salita guancia inferiore
        [475.0, 135.0],
        [485.0, 170.0],      # Musetto anteriore avanzato a protezione della plancia
        [485.0, 185.0],      # Apice arrotondato guancia
        [475.0, 198.0],
        [440.0, 215.0],      # Bordo superiore guancia
        [390.0, 245.0],      # Inizio grande gola concava arcade
        [350.0, 285.0],
        [320.0, 335.0],
        [290.0, 395.0],
        [275.0, 440.0],
        [270.0, 465.0],
        [270.0, 485.0],
        [270.0, 505.0],      # Raccordo casse / marquee
        [255.0, 550.0],      # Inclinazione marquee
        [240.0, 585.0],
        [230.0, 598.0],
        [210.0, 602.0],      # Apice frontale del tetto
        [150.0, 585.0],
        [100.0, 570.0],
        [85.0, 560.0],       # Apice posteriore del tetto cabaret
        [50.0, 470.0],       # Schienale superiore rastremato in avanti
        [25.0, 410.0],
        [0.0, 380.0],        # Raccordo schienale spiovente con schienale verticale
        [0.0, 0.0]           # Chiusura a terra
    ]
    dxf.add_polyline(side_poly, closed=True)

    # Nastro di gomma T-Molding perimetrale (spessore 2.0 mm):
    tm_contour = [
        [410.0, 0.0], [417.87, 3.4], [424.53, 8.4], [431.2, 13.4], [440.18, 34.23], [448.51, 54.23],
        [456.85, 74.23], [463.56, 94.37], [470.23, 114.37], [476.9, 134.37], [480.26, 146.12],
        [483.59, 157.78], [486.92, 169.45], [487.0, 175.0], [487.0, 180.0], [487.0, 185.0],
        [483.25, 190.55], [479.92, 194.89], [476.59, 199.22], [464.23, 205.45], [452.59, 211.11],
        [440.95, 216.76], [424.38, 226.7], [407.81, 236.65], [391.24, 246.59], [378.02, 259.81],
        [364.81, 273.02], [351.59, 286.24], [341.64, 302.81], [331.7, 319.39], [321.75, 335.96],
        [311.79, 355.9], [301.82, 375.83], [291.85, 395.77], [286.88, 410.68], [281.91, 425.6],
        [276.94, 440.51], [275.29, 448.74], [273.65, 456.97], [272.0, 465.2], [272.0, 471.8],
        [272.0, 478.4], [272.0, 485.0], [272.0, 491.67], [272.0, 498.33], [272.0, 505.0],
        [266.9, 520.63], [261.9, 535.63], [256.9, 550.63], [251.84, 562.45], [246.84, 574.12],
        [241.84, 585.79], [238.25, 590.55], [234.92, 594.89], [231.59, 599.22], [223.73, 601.29],
        [217.06, 602.63], [210.39, 603.96], [189.45, 598.26], [169.45, 592.59], [149.45, 586.92],
        [132.76, 581.92], [116.09, 576.92], [99.43, 571.92], [93.89, 568.33], [88.89, 565.0],
        [83.89, 561.66], [71.47, 530.73], [59.81, 500.74], [48.14, 470.75], [39.85, 450.85],
        [31.56, 430.95], [23.27, 411.05], [15.0, 401.13], [6.73, 391.2], [-1.54, 381.28],
        [-2.0, 253.33], [-2.0, 126.67], [-2.0, 0.0]
    ]
    dxf.add_polyline(tm_contour, closed=False, layer="TMOLDING", color=4)

    # Linee di riferimento interne (in rosso GUIDE)
    # 1. Base a terra (+22mm)
    base_p1 = [20.0, 22.0]
    base_p2 = [380.0, 22.0]
    dxf.add_line(base_p1, base_p2, layer="GUIDE", color=1)

    # 2. Frontalino Kickplate
    kp_p1 = [380.0, 41.0]
    kp_p2 = [430.0, 131.5]
    kp_dx, kp_dy = kp_p2[0]-kp_p1[0], kp_p2[1]-kp_p1[1]
    kp_L = math.hypot(kp_dx, kp_dy)
    kp_ux, kp_uy = kp_dx/kp_L, kp_dy/kp_L
    kp_nx, kp_ny = -kp_uy, kp_ux
    dxf.add_line(kp_p1, kp_p2, layer="GUIDE", color=1)

    # 3. Plancia Comandi 2P (lunghezza 204mm)
    cp_p1 = [268.0, 175.0]
    cp_p2 = [470.0, 147.5]
    cp_dx, cp_dy = cp_p2[0]-cp_p1[0], cp_p2[1]-cp_p1[1]
    cp_L = math.hypot(cp_dx, cp_dy)
    cp_ux, cp_uy = cp_dx/cp_L, cp_dy/cp_L
    cp_nx, cp_ny = -cp_uy, cp_ux
    dxf.add_line(cp_p1, cp_p2, layer="GUIDE", color=1)

    # 4. Vetro Monitor (AOC 21.5")
    scr_base = [268.0, 175.0]
    scr_top = [150.0, 470.0]
    dx_m = scr_top[0] - scr_base[0]
    dy_m = scr_top[1] - scr_base[1]
    L_m = math.hypot(dx_m, dy_m)
    u_mx = dx_m / L_m
    u_my = dy_m / L_m
    n_mx = -u_my
    n_my = u_mx
    dxf.add_line(scr_base, scr_top, layer="GUIDE", color=1)

    # Traversa VESA arretrata di 56 mm
    vesa_base = [scr_base[0] + 56.0*n_mx, scr_base[1] + 56.0*n_my]
    dxf.add_line([round(vesa_base[0] + 50*u_mx, 1), round(vesa_base[1] + 50*u_my, 1)],
                 [round(vesa_base[0] + 235*u_mx, 1), round(vesa_base[1] + 235*u_my, 1)], layer="GUIDE", color=1)

    # 5. Pannello Casse Audio (114.4mm)
    spk_rear = [150.0, 470.0]
    spk_front = [265.0, 505.0]
    spk_dx, spk_dy = spk_front[0]-spk_rear[0], spk_front[1]-spk_rear[1]
    spk_L = math.hypot(spk_dx, spk_dy)
    spk_ux, spk_uy = spk_dx/spk_L, spk_dy/spk_L
    spk_nx, spk_ny = -spk_uy, spk_ux
    dxf.add_line(spk_rear, spk_front, layer="GUIDE", color=1)

    # 6. Insegna Marquee (80.8mm)
    marq_front = [265.0, 505.0]
    marq_top = [235.0, 580.0]
    dxf.add_line(marq_front, marq_top, layer="GUIDE", color=1)

    # 7. Tetto Superiore Compatto (142.4mm)
    roof_rear = [90.0, 560.0]
    roof_front = [235.0, 580.0]
    roof_dx = roof_front[0] - roof_rear[0]
    roof_dy = roof_front[1] - roof_rear[1]
    roof_L = math.hypot(roof_dx, roof_dy)
    roof_ux = roof_dx / roof_L
    roof_uy = roof_dy / roof_L
    roof_nx = -roof_uy
    roof_ny = roof_ux
    dxf.add_line(roof_rear, roof_front, layer="GUIDE", color=1)

    # 8A. Schienale Inferiore Verticale (Z=41 a 380mm)
    dxf.add_line([20.0, 41.0], [20.0, 380.0], layer="GUIDE", color=1)

    # 8B. Schienale Superiore Spiovente (da Z=380 a sotto il tetto)
    rup_p1 = [21.29, 386.99]
    rup_p2 = [80.61, 539.53]
    rup_dx = rup_p2[0] - rup_p1[0]
    rup_dy = rup_p2[1] - rup_p1[1]
    rup_L = math.hypot(rup_dx, rup_dy)
    rup_ux = rup_dx / rup_L
    rup_uy = rup_dy / rup_L
    rup_nx = rup_uy
    rup_ny = -rup_ux
    dxf.add_line(rup_p1, rup_p2, layer="GUIDE", color=1)

    # Funzioni asole inclinate
    def make_kp_slot(t1, t2):
        return [[round(kp_p1[0] + t*kp_ux + s*th_slot*kp_nx, 1), round(kp_p1[1] + t*kp_uy + s*th_slot*kp_ny, 1)]
                for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]]

    def make_cp_slot(t1, t2):
        return [[round(cp_p1[0] + t*cp_ux - s*th_slot*cp_nx, 1), round(cp_p1[1] + t*cp_uy - s*th_slot*cp_ny, 1)]
                for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]]

    def make_vesa_slot(t1, t2):
        return [[round(vesa_base[0] + t*u_mx + s*th_slot/2*n_mx, 1), round(vesa_base[1] + t*u_my + s*th_slot/2*n_my, 1)]
                for t, s in [(t1, -1), (t2, -1), (t2, 1), (t1, 1)]]

    def make_spk_slot(t1, t2):
        return [[round(spk_rear[0] + t*spk_ux + s*th_slot*spk_nx, 1), round(spk_rear[1] + t*spk_uy + s*th_slot*spk_ny, 1)]
                for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]]

    def make_rf_slot(t1, t2):
        return [[round(roof_rear[0] + t*roof_ux - s*th_slot*roof_nx, 1), round(roof_rear[1] + t*roof_uy - s*th_slot*roof_ny, 1)]
                for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]]

    def make_rup_slot(t1, t2):
        return [[round(rup_p1[0] + t*rup_ux + s*th_slot*rup_nx, 1), round(rup_p1[1] + t*rup_uy + s*th_slot*rup_ny, 1)]
                for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]]

    # LE 12 MORTASE FEMMINA - ZERO CLASH E VERIFICATE NEL PIENO
    mortises = {
        'Base Posteriore': [[70, 22], [140, 22], [140, 22+th_slot], [70, 22+th_slot]],
        'Base Anteriore': [[250, 22], [320, 22], [320, 22+th_slot], [250, 22+th_slot]],
        'Frontalino Kickplate': make_kp_slot(15, 65),
        'Plancia Retro': make_cp_slot(30, 70),
        'Plancia Fronte': make_cp_slot(105, 145),
        'Supporto VESA Basso': make_vesa_slot(50, 95),
        'Supporto VESA Alto': make_vesa_slot(190, 235),
        'Pannello Casse Audio': make_spk_slot(25, 85),
        'Tetto Superiore': make_rf_slot(30, 105),
        'Schienale Inferiore Basso': [[20, 70], [39.2, 70], [39.2, 130], [20, 130]],
        'Schienale Inferiore Alto': [[20, 290], [39.2, 290], [39.2, 350], [20, 350]],
        'Schienale Superiore Spiovente': make_rup_slot(35, 125),
    }

    for name, pts in mortises.items():
        dxf.add_polyline(pts, closed=True)

    # Etichette Fiancata
    dxf.add_text([240, 645], "FIANCATA LATERALE CLASSIC CABARET (SX/DX)", 18, "C")
    dxf.add_text([240, 626], "602 x 485 mm - Catena Strutturale Continua a 100% Tagli Squadrati 90° (MDF 19mm)", 12, "C")
    dxf.add_text([240, 610], "Top Compatto 142mm - Schienale Alto Spiovente - Nastro Gomma T-Molding 2mm", 10, "C")
    dxf.add_text([495, 175], "T-Molding Gomma 2mm", 9, "L", layer="TMOLDING", color=4)
    dxf.add_text([190, 8], "Asole Base (+22mm da terra)", 9, "C")
    dxf.add_text([375, 75], "Asola Frontalino (Taglio 90°)", 9, "C")
    dxf.add_text([350, 180], "Asole Plancia Comandi (204mm)", 9, "C")
    dxf.add_text([120, 230], "Asole Supporto VESA (-56mm)", 9, "C")
    dxf.add_text([170, 560], "Asola Tetto (142mm)", 8, "C")
    dxf.add_text([205, 490], "Asola Casse (114mm)", 8, "C")
    dxf.add_text([250, 545], "Marquee (81mm)", 8, "C")
    dxf.add_text([65, 450], "Asola Schienale Spiovente", 9, "C")
    dxf.add_text([30, 100], "Asola Schienale Basso", 8, "C")
    dxf.add_text([30, 320], "Asola Schienale Alto", 8, "C")
    dxf.add_text([205, 330], "Vetro Monitor (AOC 21.5\")", 8, "C")

    # =========================================================================
    # COLONNA 2: PLANCIA 2P + FRONTALINO + BASE (X = 620 .. 1134)
    # =========================================================================
    ox2 = 620.0
    print("2. Plancia Comandi 2 Giocatori (Layout Sanwa), Frontalino e Base...")

    # 2A. Plancia Comandi 2 Giocatori (Y: 0 .. 204)
    # Orientamento Corretto: Y=0 Bordo Posteriore (Bezel), Y=204 Bordo Anteriore (Giocatore/Polsi)
    cp_h = 204.0
    cp_verts = [
        [ox2, 0],
        [ox2, 30], [ox2 - tenon_len, 30], [ox2 - tenon_len, 70], [ox2, 70],
        [ox2, 105], [ox2 - tenon_len, 105], [ox2 - tenon_len, 145], [ox2, 145],
        [ox2, cp_h],
        [ox2 + w_int, cp_h],
        [ox2 + w_int, 145], [ox2 + w_int + tenon_len, 145], [ox2 + w_int + tenon_len, 105], [ox2 + w_int, 105],
        [ox2 + w_int, 70], [ox2 + w_int + tenon_len, 70], [ox2 + w_int + tenon_len, 30], [ox2 + w_int, 30],
        [ox2 + w_int, 0],
        [ox2, 0]
    ]
    dxf.add_polyline(cp_verts, closed=True)
    dxf.add_line([ox2 + w_int/2, 0], [ox2 + w_int/2, cp_h], layer="GUIDE", color=1)

    # Impronta di appoggio del frontalino sottostante (Y: 147.1 .. 164.8) - ZONA CIECA PROTETTA
    dxf.add_rect([ox2, 147.1], [ox2 + w_int, 164.8], layer="GUIDE", color=1)
    dxf.add_text([ox2 + w_int/2, 154.0], "BATTUTA FRONTALINO SOTTOSTANTE (MDF 19mm - ZERO FORATURE)", 8, "C", layer="GUIDE", color=1)

    # Giocatore 2 (A Destra del mobile, X bassa verso Fiancata Destra)
    # Leva Joystick 2P a Sinistra (X = 199), 6 Tasti a Destra (X = 75..139)
    j2_x, j2_y = ox2 + 199, 90
    dxf.add_circle([j2_x, j2_y], 15.0) # Foro Joystick d=30mm
    dxf.add_circle([j2_x, j2_y], 1.5)  # Centro
    for fx in [j2_x - 42.5, j2_x + 42.5]:
        for fy in [j2_y - 20.0, j2_y + 20.0]:
            dxf.add_circle([fx, fy], 2.0)
    p2_btns = [
        (ox2 + 139, 80), (ox2 + 107, 75),  (ox2 + 75, 80),    # Fila 1 (superiore)
        (ox2 + 139, 114), (ox2 + 107, 109), (ox2 + 75, 114)   # Fila 2 (inferiore)
    ]
    for bx, by in p2_btns:
        dxf.add_circle([bx, by], 14.0)
        dxf.add_circle([bx, by], 1.0)
    dxf.add_circle([ox2 + 194, 42], 14.0) # 2P START (in alto verso schermo)
    dxf.add_circle([ox2 + 229, 36], 14.0) # 2P COIN (in alto verso schermo)
    dxf.add_text([ox2 + 194, 23], "2P START", 8, "C")
    dxf.add_text([ox2 + 229, 18], "2P COIN", 8, "C")

    # Giocatore 1 (A Sinistra del mobile, X alta verso Fiancata Sinistra)
    # Leva Joystick 1P a Sinistra (X = 429), 6 Tasti a Destra (X = 305..369)
    j1_x, j1_y = ox2 + 429, 90
    dxf.add_circle([j1_x, j1_y], 15.0) # Foro Joystick d=30mm
    dxf.add_circle([j1_x, j1_y], 1.5)  # Centro
    for fx in [j1_x - 42.5, j1_x + 42.5]:
        for fy in [j1_y - 20.0, j1_y + 20.0]:
            dxf.add_circle([fx, fy], 2.0)
    p1_btns = [
        (ox2 + 369, 80), (ox2 + 337, 75),  (ox2 + 305, 80),   # Fila 1 (superiore)
        (ox2 + 369, 114), (ox2 + 337, 109), (ox2 + 305, 114)  # Fila 2 (inferiore)
    ]
    for bx, by in p1_btns:
        dxf.add_circle([bx, by], 14.0)
        dxf.add_circle([bx, by], 1.0)
    dxf.add_circle([ox2 + 319, 42], 14.0) # 1P START (in alto verso schermo)
    dxf.add_circle([ox2 + 284, 36], 14.0) # 1P COIN (in alto verso schermo)
    dxf.add_text([ox2 + 319, 23], "1P START", 8, "C")
    dxf.add_text([ox2 + 284, 18], "1P COIN", 8, "C")

    dxf.add_text([ox2 + 130, 132], "GIOCATORE 2 (DESTRA)", 10, "C")
    dxf.add_text([ox2 + 375, 132], "GIOCATORE 1 (SINISTRA)", 10, "C")
    dxf.add_text([ox2 + 20, 10], "FIANCATA DESTRA", 8, "L")
    dxf.add_text([ox2 + w_int - 20, 10], "FIANCATA SINISTRA", 8, "R")
    dxf.add_text([ox2 + w_int/2, 185], "ZONA APPOGGIO POLSI (AGGETTO 39mm - NESSUNA FORATURA)", 9, "C")
    dxf.add_text([ox2 + w_int/2, cp_h + 10], "BORDO ANTERIORE PLANCIA (LATO GIOCATORE)", 10, "C")

    dxf.add_text([ox2 + w_int/2, -18], "BORDO POSTERIORE PLANCIA (CONTATTO BEZEL MONITOR)", 10, "C")
    dxf.add_text([ox2 + w_int/2, -34], "PLANCIA COMANDI 2 GIOCATORI (514 x 204 mm - MDF 19mm)", 14, "C")
    dxf.add_text([ox2 + w_int/2, -48], "Leve a Sinistra, Tasti a Destra per entrambi i giocatori (Zero Clash)", 9, "C")

    # 2B. Frontalino Kickplate (Y: 250 .. 345.4)
    y_front = 250.0
    kp_h = 95.4
    front_verts = [
        [ox2, y_front],
        [ox2, y_front + 15.0], [ox2 - tenon_len, y_front + 15.0], [ox2 - tenon_len, y_front + 65.0], [ox2, y_front + 65.0],
        [ox2, y_front + kp_h],
        [ox2 + w_int, y_front + kp_h],
        [ox2 + w_int, y_front + 65.0], [ox2 + w_int + tenon_len, y_front + 65.0], [ox2 + w_int + tenon_len, y_front + 15.0], [ox2 + w_int, y_front + 15.0],
        [ox2 + w_int, y_front],
        [ox2, y_front]
    ]
    dxf.add_polyline(front_verts, closed=True)
    dxf.add_circle([ox2 + 140, y_front + 47.7], 14.0) # Fori Coin d=28mm
    dxf.add_circle([ox2 + 374, y_front + 47.7], 14.0)
    dxf.add_rect([ox2 + w_int/2 - 14, y_front + 47.7 - 8], [ox2 + w_int/2 + 14, y_front + 47.7 + 8], fillet=2) # Doppia USB
    dxf.add_text([ox2 + w_int/2, y_front + kp_h + 20], "FRONTALINO INFERIORE (KICKPLATE - TAGLIO 90°)", 16, "C")
    dxf.add_text([ox2 + w_int/2, y_front + kp_h + 6], "514 x 95.4 mm (2 Tenoni Maschio da 50mm - Chiusura Sotto Plancia)", 10, "C")

    # 2C. Base Inferiore (Y: 400 .. 760)
    y_base = 400.0
    base_h = 360.0
    base_verts = [
        [ox2, y_base],
        [ox2, y_base + 50.0], [ox2 - tenon_len, y_base + 50.0], [ox2 - tenon_len, y_base + 120.0], [ox2, y_base + 120.0],
        [ox2, y_base + 230.0], [ox2 - tenon_len, y_base + 230.0], [ox2 - tenon_len, y_base + 300.0], [ox2, y_base + 300.0],
        [ox2, y_base + base_h],
        [ox2 + w_int, y_base + base_h],
        [ox2 + w_int, y_base + 300.0], [ox2 + w_int + tenon_len, y_base + 300.0], [ox2 + w_int + tenon_len, y_base + 230.0], [ox2 + w_int, y_base + 230.0],
        [ox2 + w_int, y_base + 120.0], [ox2 + w_int + tenon_len, y_base + 120.0], [ox2 + w_int + tenon_len, y_base + 50.0], [ox2 + w_int, y_base + 50.0],
        [ox2 + w_int, y_base],
        [ox2, y_base]
    ]
    dxf.add_polyline(base_verts, closed=True)
    dxf.add_circle([ox2 + 30, y_base + 30], 6.0) # Piedini gomma d=12mm
    dxf.add_circle([ox2 + w_int - 30, y_base + 30], 6.0)
    dxf.add_circle([ox2 + 30, y_base + 330], 6.0)
    dxf.add_circle([ox2 + w_int - 30, y_base + 330], 6.0)
    for sy in [y_base + 150, y_base + 185, y_base + 220]:
        dxf.add_slot([ox2 + 180, sy + 5], [ox2 + 334, sy + 5], 10.0)
    dxf.add_text([ox2 + w_int/2, y_base + base_h + 20], "BASE INFERIORE (FONDO)", 16, "C")
    dxf.add_text([ox2 + w_int/2, y_base + base_h + 6], "514 x 360 mm (4 Tenoni Maschio da 70mm - Feritoie Ventilazione + Piedini)", 10, "C")

    # =========================================================================
    # COLONNA 3: BEZEL + VESA SLOTS + CASSE AUDIO + MARQUEE (X = 1270 .. 1784)
    # =========================================================================
    ox3 = 1270.0
    print("3. Bezel, Traversa VESA con Asole Scorrevoli e Casse Audio Compatte...")

    # 3A. Bezel Vetro / Monitor (Y: 0 .. 318)
    bezel_h = 317.7
    dxf.add_rect([ox3, 0], [ox3 + w_int, bezel_h], fillet=4)
    dxf.add_rect([ox3 + 18, 23.8], [ox3 + w_int - 18, 293.8], fillet=3)
    dxf.add_line([ox3 + 18, 23.8], [ox3 + w_int - 18, 293.8], layer="GUIDE", color=1)
    dxf.add_text([ox3 + w_int/2, -18], "BEZEL VETRO / CORNICE MONITOR", 16, "C")
    dxf.add_text([ox3 + w_int/2, -34], "514 x 318 mm (Vetro Fumé / Acrilico 4mm)", 10, "C")
    dxf.add_text([ox3 + w_int/2, -48], "Finestra Utile 478 x 270 mm (Schermo AOC i2269Vwm 21.5\" 16:9)", 9, "C")

    # 3B. Traversa Supporto VESA (Y: 380 .. 680)
    y_vesa = 380.0
    vesa_h = 300.0
    vesa_verts = [
        [ox3, y_vesa],
        [ox3, y_vesa + 50], [ox3 - tenon_len, y_vesa + 50], [ox3 - tenon_len, y_vesa + 95], [ox3, y_vesa + 95],
        [ox3, y_vesa + 190], [ox3 - tenon_len, y_vesa + 190], [ox3 - tenon_len, y_vesa + 235], [ox3, y_vesa + 235],
        [ox3, y_vesa + vesa_h],
        [ox3 + w_int, y_vesa + vesa_h],
        [ox3 + w_int, y_vesa + 235], [ox3 + w_int + tenon_len, y_vesa + 235], [ox3 + w_int + tenon_len, y_vesa + 190], [ox3 + w_int, y_vesa + 190],
        [ox3 + w_int, y_vesa + 95], [ox3 + w_int + tenon_len, y_vesa + 95], [ox3 + w_int + tenon_len, y_vesa + 50], [ox3 + w_int, y_vesa + 50],
        [ox3 + w_int, y_vesa],
        [ox3, y_vesa]
    ]
    dxf.add_polyline(vesa_verts, closed=True)

    # Asole scorrevoli VESA 75/100
    dxf.add_slot([ox3 + 147, y_vesa + 200], [ox3 + 367, y_vesa + 200], 5.5)
    dxf.add_slot([ox3 + 147, y_vesa + 125], [ox3 + 367, y_vesa + 125], 5.5)
    dxf.add_slot([ox3 + 147, y_vesa + 100], [ox3 + 367, y_vesa + 100], 5.5)

    dxf.add_circle([ox3 + w_int/2, y_vesa + 160], 25.0) # Foro passacavi d=50mm
    dxf.add_rect([ox3 + 160, y_vesa + 40], [ox3 + 354, y_vesa + 85], fillet=8)
    for sy in [y_vesa + 110, y_vesa + 155, y_vesa + 200]:
        dxf.add_slot([ox3 + 70, sy], [ox3 + 125, sy], 12.0)
        dxf.add_slot([ox3 + w_int - 125, sy], [ox3 + w_int - 70, sy], 12.0)

    dxf.add_text([ox3 + w_int/2, y_vesa + vesa_h + 20], "TRAVERSA SUPPORTO VESA", 16, "C")
    dxf.add_text([ox3 + w_int/2, y_vesa + vesa_h + 6], "514 x 300 mm (Asole Scorrevoli Universali VESA 75/100 + Passacavi)", 10, "C")

    # 3C. Pannello Casse Audio Compatto (114.4mm) (Y: 730 .. 844.4)
    y_casse = 730.0
    casse_h = 114.4
    casse_verts = [
        [ox3, y_casse],
        [ox3, y_casse + 25.0], [ox3 - tenon_len, y_casse + 25.0], [ox3 - tenon_len, y_casse + 85.0], [ox3, y_casse + 85.0],
        [ox3, y_casse + casse_h],
        [ox3 + w_int, y_casse + casse_h],
        [ox3 + w_int, y_casse + 85.0], [ox3 + w_int + tenon_len, y_casse + 85.0], [ox3 + w_int + tenon_len, y_casse + 25.0], [ox3 + w_int, y_casse + 25.0],
        [ox3 + w_int, y_casse],
        [ox3, y_casse]
    ]
    dxf.add_polyline(casse_verts, closed=True)

    def draw_cabaret_speaker_grille(cx, cy):
        slot_lens = [36.0, 56.0, 72.0, 72.0, 56.0, 36.0]
        for idx, slen in enumerate(slot_lens):
            sy = cy - 25.0 + idx * 10.0
            dxf.add_slot([cx - slen/2, sy], [cx + slen/2, sy], 3.8)
        for fx in [cx - 30, cx + 30]:
            for fy in [cy - 30, cy + 30]:
                dxf.add_circle([fx, fy], 2.0)

    draw_cabaret_speaker_grille(ox3 + 120, y_casse + 57.0)
    draw_cabaret_speaker_grille(ox3 + w_int - 120, y_casse + 57.0)
    dxf.add_circle([ox3 + w_int/2, y_casse + 57.0], 4.0)

    dxf.add_text([ox3 + w_int/2, y_casse + casse_h + 20], "PANNELLO CASSE AUDIO (TAGLIO 90° - ZERO GAP)", 16, "C")
    dxf.add_text([ox3 + w_int/2, y_casse + casse_h + 6], "514 x 114.4 mm (2 Tenoni da 60mm - Spazio per Altoparlanti 3\"/4\")", 10, "C")

    # 3D. Marquee Superiore (80.8mm) (Y: 910 .. 990.8)
    y_marq = 910.0
    marq_h = 80.8
    dxf.add_rect([ox3, y_marq], [ox3 + w_int, y_marq + marq_h], fillet=4)
    dxf.add_text([ox3 + w_int/2, y_marq + marq_h + 20], "INSEGNA MARQUEE SUPERIORE (CLASSIC CABARET)", 16, "C")
    dxf.add_text([ox3 + w_int/2, y_marq + marq_h + 6], "514 x 80.8 mm (Plexiglass Opalino retroilluminato LED)", 10, "C")

    # =========================================================================
    # COLONNA 4: TETTO + SCHIENALI (INFERIORE E SUPERIORE SPIOVENTE) (X = 1920 .. 2434)
    # =========================================================================
    ox4 = 1920.0
    print("4. Tetto Compatto ~142mm e Doppio Schienale (Verticale + Spiovente)...")

    # 4A. Tetto Superiore Compatto Classic Cabaret (Y: 0 .. 142.4)
    roof_h = 142.4
    roof_verts = [
        [ox4, 0],
        [ox4, 30.0], [ox4 - tenon_len, 30.0], [ox4 - tenon_len, 105.0], [ox4, 105.0],
        [ox4, roof_h],
        [ox4 + w_int, roof_h],
        [ox4 + w_int, 105.0], [ox4 + w_int + tenon_len, 105.0], [ox4 + w_int + tenon_len, 30.0], [ox4 + w_int, 30.0],
        [ox4 + w_int, 0],
        [ox4, 0]
    ]
    dxf.add_polyline(roof_verts, closed=True)
    for vy in [50, 95]:
        dxf.add_slot([ox4 + 130, vy], [ox4 + 384, vy], 12.0)
    dxf.add_text([ox4 + w_int/2, -18], "TETTO SUPERIORE COMPATTO (CLASSIC CABARET - TAGLIO 90°)", 16, "C")
    dxf.add_text([ox4 + w_int/2, -34], "514 x 142.4 mm (2 Tenoni Maschio da 75mm - Chiusura Cieca Superiore)", 10, "C")
    dxf.add_text([ox4 + w_int/2, -48], "2 Feritoie Orizzontali di Dissipazione Calore Naturale", 9, "C")

    # 4B. Schienale Inferiore Verticale con Presa IEC e Vano Sportello (Y: 200 .. 539)
    y_low = 200.0
    low_h = 339.0
    low_verts = [
        [ox4, y_low],
        [ox4, y_low + 29.0], [ox4 - tenon_len, y_low + 29.0], [ox4 - tenon_len, y_low + 89.0], [ox4, y_low + 89.0],
        [ox4, y_low + 249.0], [ox4 - tenon_len, y_low + 249.0], [ox4 - tenon_len, y_low + 309.0], [ox4, y_low + 309.0],
        [ox4, y_low + low_h],
        [ox4 + w_int, y_low + low_h],
        [ox4 + w_int, y_low + 309.0], [ox4 + w_int + tenon_len, y_low + 309.0], [ox4 + w_int + tenon_len, y_low + 249.0], [ox4 + w_int, y_low + 249.0],
        [ox4 + w_int, y_low + 89.0], [ox4 + w_int + tenon_len, y_low + 89.0], [ox4 + w_int + tenon_len, y_low + 29.0], [ox4 + w_int, y_low + 29.0],
        [ox4 + w_int, y_low],
        [ox4, y_low]
    ]
    dxf.add_polyline(low_verts, closed=True)

    # Vano sportello inferiore (434 x 220 mm)
    dxf.add_rect([ox4 + 40, y_low + 104.0], [ox4 + 474, y_low + 324.0], fillet=4)
    dxf.add_text([ox4 + w_int/2, y_low + 214.0], "VANO SPORTELLO INFERIORE (434 x 220 mm)", 12, "C")

    # Presa 220V IEC C14 ALZATA a Z=85 (44mm sopra fondo base)
    y_plug = y_low + 44.0
    dxf.add_rect([ox4 + w_int/2 - 24, y_plug - 14], [ox4 + w_int/2 + 24, y_plug + 14], fillet=2)
    dxf.add_circle([ox4 + w_int/2 - 20, y_plug], 1.75)
    dxf.add_circle([ox4 + w_int/2 + 20, y_plug], 1.75)
    dxf.add_text([ox4 + w_int/2, y_plug - 22], "PRESA ALIMENTAZIONE 220V IEC C14 ALZATA (Z=85)", 10, "C")

    dxf.add_text([ox4 + w_int/2, y_low + low_h + 20], "SCHIENALE INFERIORE VERTICALE", 16, "C")
    dxf.add_text([ox4 + w_int/2, y_low + low_h + 6], "514 x 339 mm (4 Tenoni Maschio da 60mm - Doppio Ancoraggio)", 10, "C")

    # 4C. Schienale Superiore Spiovente (Classic Cabaret) (Y: 600 .. 763.6)
    y_rup = 600.0
    rup_h = 163.6
    rup_verts = [
        [ox4, y_rup],
        [ox4, y_rup + 35.0], [ox4 - tenon_len, y_rup + 35.0], [ox4 - tenon_len, y_rup + 125.0], [ox4, y_rup + 125.0],
        [ox4, y_rup + rup_h],
        [ox4 + w_int, y_rup + rup_h],
        [ox4 + w_int, y_rup + 125.0], [ox4 + w_int + tenon_len, y_rup + 125.0], [ox4 + w_int + tenon_len, y_rup + 35.0], [ox4 + w_int, y_rup + 35.0],
        [ox4 + w_int, y_rup],
        [ox4, y_rup]
    ]
    dxf.add_polyline(rup_verts, closed=True)
    for vy in [y_rup + 45, y_rup + 85, y_rup + 125]:
        dxf.add_slot([ox4 + 130, vy], [ox4 + 384, vy], 10.0)

    dxf.add_text([ox4 + w_int/2, y_rup + rup_h + 20], "SCHIENALE SUPERIORE SPIOVENTE (CABARET)", 16, "C")
    dxf.add_text([ox4 + w_int/2, y_rup + rup_h + 6], "514 x 163.6 mm (2 Tenoni da 90mm - 3 Feritoie Calore - Taglio 90°)", 10, "C")

    # =========================================================================
    # COLONNA 5: SPORTELLO CENTRALE INDIPENDENTE (X = 2570 .. 3000, Y = 200 .. 416)
    # =========================================================================
    ox5 = 2570.0
    y_door = 200.0
    w_door = 430.0
    door_h = 216.0
    print("5. Sportello Posteriore con Ventola 120mm e Serratura...")
    dxf.add_rect([ox5, y_door], [ox5 + w_door, y_door + door_h], fillet=4)

    cx_door = ox5 + w_door / 2
    cy_door = y_door + door_h / 2
    dxf.add_circle([cx_door, cy_door], 60.0) # Foro ventola d=120mm
    dxf.add_circle([cx_door, cy_door], 30.0)
    for fx in [cx_door - 52.5, cx_door + 52.5]:
        for fy in [cy_door - 52.5, cy_door + 52.5]:
            dxf.add_circle([fx, fy], 2.25)
    dxf.add_text([cx_door, cy_door - 75], "VENTOLA SILENZIOSA 120mm AL CENTRO", 11, "C")

    # Serratura a cilindro d=19mm
    dxf.add_circle([ox5 + w_door - 30, y_door + 160.0], 9.5)
    dxf.add_text([ox5 + w_door - 30, y_door + 185.0], "SERRATURA (d=19)", 9, "C")

    # Incavi per 2 cerniere a libro sul bordo sinistro
    dxf.add_rect([ox5, y_door + 30], [ox5 + 10, y_door + 70])
    dxf.add_rect([ox5, y_door + 146], [ox5 + 10, y_door + 186])

    dxf.add_text([ox5 + w_door/2, y_door + door_h + 20], "SPORTELLO INFERIORE DI MANUTENZIONE", 16, "C")
    dxf.add_text([ox5 + w_door/2, y_door + door_h + 6], "430 x 216 mm (Ventola 120mm, Serratura e Cerniere)", 10, "C")

    dxf.save()

if __name__ == "__main__":
    out_file = "/home/paolo/Projects/cabinato/cabinato_arcade_cadcraft.dxf"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    build_cabinet_lep1_project(out_file)
