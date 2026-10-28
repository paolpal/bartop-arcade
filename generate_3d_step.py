#!/usr/bin/env python3
"""
Generatore Modello 3D STEP per Cabinato Arcade Bartop 2P (Configurazione Classic Cabaret)
- Top Accorciato a ~150mm: Silhouette rastremata sul retro e marquee compatto
- Tagli Pannelli al 100% a 90°: Nessun taglio obliquo/miter, tutti i bordi squadrati a 90°
- Nastro di Gomma (T-Molding): Profilo perimetrale in gomma da 2mm su entrambe le fiancate
- Solidi 3D Perfetti: Esattamente 16 parti unificate (14 pannelli/hardware + 2 T-molding)
- Zero Collisioni: Volume di intersezione = 0.000 mm3 tra tutte le coppie
- Zero Buchi / Gap: Contatto continuo da Frontalino a Plancia, Bezel, Casse, Marquee, Tetto e Schienali
- Sanwa Tondi: Fori joystick (d=30mm) e tasti (d=28mm) perfettamente cilindrici
- Presa IEC Rialzata: Quota Z=85mm (44mm sopra il fondo), vano retrostante libero
- Plancia Allungata: Estesa a X=470mm con aggetto frontale ergonomico per i polsi
"""

import math
import os
import sys
import numpy as np
from build123d import *
from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeOffset
from OCP.GeomAbs import GeomAbs_JoinType
from OCP.TopoDS import TopoDS

def build_perfect_arcade_model(out_step="/home/paolo/Projects/cabinato/cabinato_arcade_3d.step"):
    print("=== COSTRUZIONE MODELLO 3D (CLASSIC CABARET TOP ~150MM - TAGLI 90° + T-MOLDING) ===")
    
    th = 19.0           # Spessore pannelli MDF
    w_int = 514.0       # Larghezza interna netta
    tenon_len = 19.0    # Tenoni a filo esterno della fiancata
    th_slot = 19.2      # Tolleranza mortasa (+0.2mm)
    
    # Helper per restringere leggermente i tenoni rispetto alle mortase (0.25mm di aria)
    def shrink_tenon(pts, inset=0.25):
        pts_arr = np.array(pts, dtype=float)
        center = np.mean(pts_arr, axis=0)
        shrunk = []
        for p in pts_arr:
            d = p - center
            L = np.linalg.norm(d)
            shrunk.append(tuple(p - (d/L)*inset))
        return shrunk

    def make_panel(body_pts, mortise_list, label):
        bw = Wire.make_polygon([Vector(0, y, z) for y, z in body_pts])
        p_body = extrude(Face(bw), amount=w_int, dir=Vector(1, 0, 0))
        for m_pts in mortise_list:
            t_pts = shrink_tenon(m_pts, inset=0.25)
            tw = Wire.make_polygon([Vector(0, y, z) for y, z in t_pts])
            tf = Face(tw)
            t_left = extrude(tf, amount=tenon_len, dir=Vector(1, 0, 0)).moved(Location(Vector(-tenon_len, 0, 0)))
            t_right = extrude(tf, amount=tenon_len, dir=Vector(1, 0, 0)).moved(Location(Vector(w_int, 0, 0)))
            p_body = p_body + t_left + t_right
        p_body.label = label
        return p_body

    # -------------------------------------------------------------------------
    # 1. BASE INFERIORE (100% Rettangolo a 90°)
    # -------------------------------------------------------------------------
    base_poly = [(20.0, 22.0), (380.0, 22.0), (380.0, 41.0), (20.0, 41.0)]
    m_base1 = [(70.0, 22.0), (140.0, 22.0), (140.0, 22.0+th_slot), (70.0, 22.0+th_slot)]
    m_base2 = [(250.0, 22.0), (320.0, 22.0), (320.0, 22.0+th_slot), (250.0, 22.0+th_slot)]

    # -------------------------------------------------------------------------
    # 2. PLANCIA COMANDI 2P (100% Rettangolo a 90°, allungata a X=470mm)
    # -------------------------------------------------------------------------
    cp_p1 = (268.0, 175.0)
    cp_p2 = (470.0, 147.5)
    cp_dx = cp_p2[0] - cp_p1[0]
    cp_dz = cp_p2[1] - cp_p1[1]
    cp_L = math.hypot(cp_dx, cp_dz)
    cp_u = (cp_dx/cp_L, cp_dz/cp_L)
    cp_n = (-cp_u[1], cp_u[0])
    cp_angle = math.degrees(math.atan2(cp_u[1], cp_u[0]))

    cp_poly = [
        cp_p1,
        cp_p2,
        (cp_p2[0] - th*cp_n[0], cp_p2[1] - th*cp_n[1]),
        (cp_p1[0] - th*cp_n[0], cp_p1[1] - th*cp_n[1])
    ]

    def make_cp_slot(t1, t2, w=th_slot):
        return [(cp_p1[0] + t*cp_u[0] - s*w*cp_n[0],
                 cp_p1[1] + t*cp_u[1] - s*w*cp_n[1])
                for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]]
    m_cp1 = make_cp_slot(30.0, 70.0)
    m_cp2 = make_cp_slot(115.0, 165.0)

    # -------------------------------------------------------------------------
    # 3. FRONTALINO KICKPLATE (100% Rettangolo a 90°, chiusura sotto plancia)
    # -------------------------------------------------------------------------
    kp_p1 = np.array([380.0, 41.05])
    kp_dir = np.array([50.0, 90.0])
    kp_u = kp_dir / np.linalg.norm(kp_dir)
    kp_n = np.array([-kp_u[1], kp_u[0]])
    kp_angle = math.degrees(math.atan2(kp_u[1], kp_u[0]))

    P_cp_bot = np.array(cp_p1) - th * np.array(cp_n)
    denom = np.dot(kp_u, cp_n)
    numer = np.dot(P_cp_bot - kp_p1 - th*kp_n, cp_n) - 0.05
    L_kp = numer / denom

    P_top_front = kp_p1 + L_kp * kp_u
    P_top_rear = P_top_front + th * kp_n
    P_bot_rear = kp_p1 + th * kp_n

    kp_poly = [
        tuple(kp_p1),
        tuple(P_top_front),
        tuple(P_top_rear),
        tuple(P_bot_rear)
    ]

    m_kp = [
        (kp_p1[0] + 15.0*kp_u[0], kp_p1[1] + 15.0*kp_u[1]),
        (kp_p1[0] + 65.0*kp_u[0], kp_p1[1] + 65.0*kp_u[1]),
        (kp_p1[0] + 65.0*kp_u[0] + th_slot*kp_n[0], kp_p1[1] + 65.0*kp_u[1] + th_slot*kp_n[1]),
        (kp_p1[0] + 15.0*kp_u[0] + th_slot*kp_n[0], kp_p1[1] + 15.0*kp_u[1] + th_slot*kp_n[1])
    ]

    # -------------------------------------------------------------------------
    # 4. INSEGNA MARQUEE (Plexiglass 4mm, 100% Rettangolo a 90°, quota X=265 a 235)
    # -------------------------------------------------------------------------
    mq_p1 = (265.0, 505.0)
    mq_p2 = (235.0, 580.0)
    mq_dx = mq_p2[0] - mq_p1[0]
    mq_dz = mq_p2[1] - mq_p1[1]
    mq_L = math.hypot(mq_dx, mq_dz)
    mq_u = (mq_dx/mq_L, mq_dz/mq_L)
    mq_n = (-mq_u[1], mq_u[0])
    mq_poly = [
        mq_p1, mq_p2,
        (mq_p2[0] + 4.0*mq_n[0], mq_p2[1] + 4.0*mq_n[1]),
        (mq_p1[0] + 4.0*mq_n[0], mq_p1[1] + 4.0*mq_n[1])
    ]

    # -------------------------------------------------------------------------
    # 5. PANNELLO CASSE AUDIO (100% Rettangolo a 90°, da monitor a marquee)
    # -------------------------------------------------------------------------
    spk_rear_bot = (150.0, 470.0)
    P_mq_inner = (mq_p1[0] + 4.1*mq_n[0], mq_p1[1] + 4.1*mq_n[1])
    spk_dx = P_mq_inner[0] - spk_rear_bot[0]
    spk_dz = P_mq_inner[1] - spk_rear_bot[1]
    spk_L_full = math.hypot(spk_dx, spk_dz)
    spk_u = (spk_dx/spk_L_full, spk_dz/spk_L_full)
    spk_n = (-spk_u[1], spk_u[0])
    spk_angle = math.degrees(math.atan2(spk_u[1], spk_u[0]))

    A_spk = np.array([[spk_u[0], -mq_u[0]], [spk_u[1], -mq_u[1]]])
    b_spk = np.array([P_mq_inner[0] - (spk_rear_bot[0] + th*spk_n[0]),
                      P_mq_inner[1] - (spk_rear_bot[1] + th*spk_n[1])])
    s_max, _ = np.linalg.solve(A_spk, b_spk)
    spk_L_90 = s_max - 0.05
    spk_p_front = (spk_rear_bot[0] + spk_L_90*spk_u[0], spk_rear_bot[1] + spk_L_90*spk_u[1])

    spk_poly = [
        spk_rear_bot,
        spk_p_front,
        (spk_p_front[0] + th*spk_n[0], spk_p_front[1] + th*spk_n[1]),
        (spk_rear_bot[0] + th*spk_n[0], spk_rear_bot[1] + th*spk_n[1])
    ]

    def make_spk_slot(t1, t2):
        return [
            (spk_rear_bot[0] + t*spk_u[0] + s*th_slot*spk_n[0],
             spk_rear_bot[1] + t*spk_u[1] + s*th_slot*spk_n[1])
            for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]
        ]
    m_spk = make_spk_slot(25.0, 85.0)

    # -------------------------------------------------------------------------
    # 6. SCHIENALE INFERIORE VERTICALE (Z=41 a 380mm) & SCHIENALE SUPERIORE SPIOVENTE
    # -------------------------------------------------------------------------
    rear_low_poly = [(20.0, 41.0), (39.0, 41.0), (39.0, 380.0), (20.0, 380.0)]
    m_rlow1 = [(20.0, 70.0), (39.0, 70.0), (39.0, 130.0), (20.0, 130.0)]
    m_rlow2 = [(20.0, 290.0), (39.0, 290.0), (39.0, 350.0), (20.0, 350.0)]

    # Schienale Superiore Spiovente: da quota 380 a sotto la faccia inferiore del Tetto
    rup_u = np.array([70.0, 180.0])
    rup_u = rup_u / np.linalg.norm(rup_u)
    rup_n = np.array([-rup_u[1], rup_u[0]])
    rup_n_in = -rup_n
    rup_angle = math.degrees(math.atan2(rup_u[1], rup_u[0]))

    P_in_bot = np.array([39.0, 380.1])
    P_out_bot = P_in_bot - th * rup_n_in

    # Roof geometry definition (to align roof bottom and rear top with 0 clash)
    rf_p2 = np.array([90.0, 560.0])
    rf_p1_dir = np.array([235.0, 580.0])
    rf_dx = rf_p1_dir[0] - rf_p2[0]
    rf_dz = rf_p1_dir[1] - rf_p2[1]
    rf_L = math.hypot(rf_dx, rf_dz)
    rf_u = np.array([rf_dx/rf_L, rf_dz/rf_L])
    rf_n = np.array([-rf_u[1], rf_u[0]])
    rf_angle = math.degrees(math.atan2(rf_u[1], rf_u[0]))

    t_out = np.dot(rf_p2 - th*rf_n - P_out_bot, rf_n) / np.dot(rup_u, rf_n)
    t_out_safe = t_out - 0.1
    P_out_top = P_out_bot + t_out_safe * rup_u
    P_in_top = P_out_top + th * rup_n_in

    rup_poly = [tuple(P_out_bot), tuple(P_out_top), tuple(P_in_top), tuple(P_in_bot)]

    def make_rup_slot(t1, t2):
        p_base_origin = P_out_bot
        return [
            (p_base_origin[0] + t*rup_u[0] + s*th_slot*rup_n_in[0],
             p_base_origin[1] + t*rup_u[1] + s*th_slot*rup_n_in[1])
            for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]
        ]
    m_rup = make_rup_slot(35.0, 125.0)

    # -------------------------------------------------------------------------
    # 7. TETTO SUPERIORE COMPATTO (~142mm, da quota 90, 560 a marquee)
    # -------------------------------------------------------------------------
    P_mq_top_inner = (mq_p2[0] + 4.1*mq_n[0], mq_p2[1] + 4.1*mq_n[1])
    rf_L_90 = (P_mq_top_inner[0] - 90.0) / rf_u[0] - 0.15
    rf_p_front = (90.0 + rf_L_90*rf_u[0], 560.0 + rf_L_90*rf_u[1])

    rf_poly = [
        tuple(rf_p2),
        tuple(rf_p_front),
        (rf_p_front[0] - th*rf_n[0], rf_p_front[1] - th*rf_n[1]),
        (rf_p2[0] - th*rf_n[0], rf_p2[1] - th*rf_n[1])
    ]

    def make_rf_slot(t1, t2):
        return [
            (rf_p2[0] + t*rf_u[0] - s*th_slot*rf_n[0],
             rf_p2[1] + t*rf_u[1] - s*th_slot*rf_n[1])
            for t, s in [(t1, 0), (t2, 0), (t2, 1), (t1, 1)]
        ]
    m_rf = make_rf_slot(30.0, 105.0)

    # -------------------------------------------------------------------------
    # 8. BEZEL MONITOR, SCHERMO LCD AOC 21.5" E TRAVERSA VESA
    # -------------------------------------------------------------------------
    scr_base = (268.0, 175.0)
    scr_top = (150.0, 470.0)
    scr_dx = scr_top[0] - scr_base[0]
    scr_dz = scr_top[1] - scr_base[1]
    scr_L = math.hypot(scr_dx, scr_dz)
    scr_u = (scr_dx/scr_L, scr_dz/scr_L)
    scr_n = (-scr_u[1], scr_u[0])
    scr_angle = math.degrees(math.atan2(scr_u[1], scr_u[0]))

    bz_poly = [
        scr_base,
        scr_top,
        (scr_top[0] + 4.0*scr_n[0], scr_top[1] + 4.0*scr_n[1]),
        (scr_base[0] + 4.0*scr_n[0], scr_base[1] + 4.0*scr_n[1])
    ]

    vesa_base = (scr_base[0] + 56.0*scr_n[0], scr_base[1] + 56.0*scr_n[1])
    vesa_p1 = vesa_base
    vesa_p2 = (vesa_base[0] + 300.0*scr_u[0], vesa_base[1] + 300.0*scr_u[1])
    vesa_poly = [
        (vesa_p1[0] - th/2*scr_n[0], vesa_p1[1] - th/2*scr_n[1]),
        (vesa_p2[0] - th/2*scr_n[0], vesa_p2[1] - th/2*scr_n[1]),
        (vesa_p2[0] + th/2*scr_n[0], vesa_p2[1] + th/2*scr_n[1]),
        (vesa_p1[0] + th/2*scr_n[0], vesa_p1[1] + th/2*scr_n[1])
    ]

    def make_vesa_slot(t1, t2):
        return [
            (vesa_base[0] + t*scr_u[0] + s*th_slot/2*scr_n[0],
             vesa_base[1] + t*scr_u[1] + s*th_slot/2*scr_n[1])
            for t, s in [(t1, -1), (t2, -1), (t2, 1), (t1, 1)]
        ]
    m_vesa1 = make_vesa_slot(50.0, 95.0)
    m_vesa2 = make_vesa_slot(190.0, 235.0)

    # -------------------------------------------------------------------------
    # 9. FIANCATA SILHOUETTE (Piano YZ) CON LE 11 MORTASE (CLASSIC CABARET)
    # -------------------------------------------------------------------------
    side_poly = [
        (0.0, 0.0), (410.0, 0.0), (430.0, 15.0), (455.0, 75.0), (475.0, 135.0),
        (485.0, 170.0), (485.0, 185.0), (475.0, 198.0), (440.0, 215.0),
        (390.0, 245.0), (350.0, 285.0), (320.0, 335.0), (290.0, 395.0),
        (275.0, 440.0), (270.0, 465.0), (270.0, 485.0), (270.0, 505.0),
        (255.0, 550.0), (240.0, 585.0), (230.0, 598.0), (210.0, 602.0),
        (150.0, 585.0), (100.0, 570.0), (85.0, 560.0), (50.0, 470.0),
        (25.0, 410.0), (0.0, 380.0), (0.0, 0.0)
    ]
    fiancata_face = Face(Wire.make_polygon([Vector(0, y, z) for y, z in side_poly]))
    mortises_all = [
        m_base1, m_base2, m_kp, m_cp1, m_cp2,
        m_vesa1, m_vesa2, m_spk, m_rf,
        m_rlow1, m_rlow2, m_rup
    ]
    for m in mortises_all:
        fiancata_face = fiancata_face - Face(Wire.make_polygon([Vector(0, y, z) for y, z in m]))

    fiancata_dx = extrude(fiancata_face, amount=th, dir=Vector(1, 0, 0)).moved(Location(Vector(-th, 0, 0)))
    fiancata_dx.label = "Fiancata_Destra"
    fiancata_sx = extrude(fiancata_face, amount=th, dir=Vector(1, 0, 0)).moved(Location(Vector(w_int, 0, 0)))
    fiancata_sx.label = "Fiancata_Sinistra"

    # -------------------------------------------------------------------------
    # 10. T-MOLDING (NASTRO DI GOMMA 2mm SUI BORDI ESTERNI DELLE FIANCATE)
    # -------------------------------------------------------------------------
    wire_inner = Wire.make_polygon([Vector(0, y, z) for y, z in side_poly])
    offset_builder = BRepOffsetAPI_MakeOffset()
    offset_builder.Init(GeomAbs_JoinType.GeomAbs_Arc)
    offset_builder.AddWire(wire_inner.wrapped)
    offset_builder.Perform(2.0)
    outer_wire = Wire(TopoDS.Wire(offset_builder.Shape()))
    f_ribbon = Face(outer_wire) - Face(wire_inner)

    bottom_cut = Face(Wire.make_polygon([
        Vector(0, -50, -50), Vector(0, 500, -50),
        Vector(0, 500, 0), Vector(0, -50, 0), Vector(0, -50, -50)
    ]))
    f_tm = f_ribbon - bottom_cut

    tm_dx = extrude(f_tm, amount=th, dir=Vector(1, 0, 0)).moved(Location(Vector(-th, 0, 0)))
    tm_dx.label = "T_Molding_Fiancata_Destra"
    tm_sx = extrude(f_tm, amount=th, dir=Vector(1, 0, 0)).moved(Location(Vector(w_int, 0, 0)))
    tm_sx.label = "T_Molding_Fiancata_Sinistra"

    # Generazione solidi dei pannelli
    p_base = make_panel(base_poly, [m_base1, m_base2], "Base_Inferiore")
    p_cp = make_panel(cp_poly, [m_cp1, m_cp2], "Plancia_Comandi_2P")
    p_kp = make_panel(kp_poly, [m_kp], "Frontalino_Kickplate")
    p_vesa = make_panel(vesa_poly, [m_vesa1, m_vesa2], "Traversa_Supporto_VESA")
    p_mq = extrude(Face(Wire.make_polygon([Vector(0, y, z) for y, z in mq_poly])), amount=w_int, dir=Vector(1, 0, 0))
    p_mq.label = "Insegna_Marquee"
    p_spk = make_panel(spk_poly, [m_spk], "Pannello_Casse_Audio")
    p_roof = make_panel(rf_poly, [m_rf], "Tetto_Superiore")
    p_rear_low = make_panel(rear_low_poly, [m_rlow1, m_rlow2], "Schienale_Inferiore_Verticale")
    p_rear_up = make_panel(rup_poly, [m_rup], "Schienale_Superiore_Spiovente")
    p_bezel = extrude(Face(Wire.make_polygon([Vector(0, y, z) for y, z in bz_poly])), amount=w_int, dir=Vector(1, 0, 0))
    p_bezel.label = "Bezel_Monitor"

    # Schermo LCD AOC 21.5" (310 x 500 x 35 mm, a 90°)
    lcd = Box(500.0, 35.0, 310.0).moved(Location(Rotation(scr_angle+90, 0, 0)))
    lcd = lcd.moved(Location(Vector(w_int/2, 187.19, 318.86)))
    lcd.label = "Schermo_LCD_AOC"

    # Sportello Posteriore di Manutenzione (430 x 220 x 19 mm, nel vano inferiore)
    p_door = Box(430.0, th, 220.0).moved(Location(Vector(w_int/2, 29.5, 250.0)))
    p_door.label = "Sportello_Posteriore"

    # -------------------------------------------------------------------------
    # 11. LAVORAZIONI E FORATURE DETTAGLIATE
    # -------------------------------------------------------------------------
    # Base: piedini e ventilazione
    base_cuts = []
    for fx, fy in [(30, 50), (w_int-30, 50), (30, 350), (w_int-30, 350)]:
        base_cuts.append(Cylinder(6.0, 30.0).moved(Location(Vector(fx, fy, 31.5))))
    for sy in [170, 205, 240]:
        base_cuts.append(Box(154.0, 10.0, 30.0).moved(Location(Vector(w_int/2, sy, 31.5))))
    p_base = p_base - Compound(base_cuts)

    # Plancia: fori Sanwa tondi (visti dal giocatore in piedi davanti al cabinato)
    # Vista Giocatore: P1 a SINISTRA, P2 a DESTRA.
    # Per ciascun giocatore: Leva/Joystick a SINISTRA, Tasti Azione a DESTRA!
    # Tasti Admin (Start/Coin) in ALTO (verso schermo), Appoggio polsi pulito in BASSO (verso giocatore).
    cp_holes = []
    def add_sanwa_round_hole(x_across, t_along, radius=14.0):
        py = cp_p1[0] + t_along * cp_u[0]
        pz = cp_p1[1] + t_along * cp_u[1]
        cyl = Cylinder(radius, 50.0).moved(Location(Rotation(cp_angle, 0, 0)))
        cyl = cyl.moved(Location(Vector(x_across, py, pz)))
        return cyl

    # GIOCATORE 1 (A SINISTRA DEL MOBILE: X=514 è la spalla sinistra del giocatore)
    # Leva Joystick 1P a SINISTRA (X = 429mm, a 85mm dal fianco sinistro)
    cp_holes.append(add_sanwa_round_hole(429.0, 90.0, 15.0))
    for fx in [429.0 - 42.5, 429.0 + 42.5]:
        for ft in [90.0 - 20.0, 90.0 + 20.0]:
            cp_holes.append(add_sanwa_round_hole(fx, ft, 2.0))

    # Tasti Azione 1P a DESTRA della leva (X = 369, 337, 305mm)
    p1_btns = [
        (369.0, 80.0), (337.0, 75.0), (305.0, 80.0),    # Fila 1 (superiore)
        (369.0, 114.0), (337.0, 109.0), (305.0, 114.0), # Fila 2 (inferiore)
        (319.0, 42.0),                                   # 1P START (in alto, zona schermo)
        (284.0, 36.0)                                    # 1P COIN (in alto, zona schermo)
    ]
    for bx, by in p1_btns:
        cp_holes.append(add_sanwa_round_hole(bx, by, 14.0))

    # GIOCATORE 2 (A DESTRA DEL MOBILE: X=0 è la spalla destra del giocatore)
    # Leva Joystick 2P a SINISTRA (X = 199mm, a sinistra dei propri tasti)
    cp_holes.append(add_sanwa_round_hole(199.0, 90.0, 15.0))
    for fx in [199.0 - 42.5, 199.0 + 42.5]:
        for ft in [90.0 - 20.0, 90.0 + 20.0]:
            cp_holes.append(add_sanwa_round_hole(fx, ft, 2.0))

    # Tasti Azione 2P a DESTRA della leva (X = 139, 107, 75mm)
    p2_btns = [
        (139.0, 80.0), (107.0, 75.0), (75.0, 80.0),     # Fila 1 (superiore)
        (139.0, 114.0), (107.0, 109.0), (75.0, 114.0),  # Fila 2 (inferiore)
        (194.0, 42.0),                                   # 2P START (in alto, zona schermo)
        (229.0, 36.0)                                    # 2P COIN (in alto, zona schermo)
    ]
    for bx, by in p2_btns:
        cp_holes.append(add_sanwa_round_hole(bx, by, 14.0))

    p_cp = p_cp - Compound(cp_holes)

    # Frontalino: 2 fori Coin + USB
    kp_mid_y = (kp_p1[0] + P_top_front[0])/2.0
    kp_mid_z = (kp_p1[1] + P_top_front[1])/2.0
    kp_cuts = []
    for cx in [140.0, w_int - 140.0]:
        c = Cylinder(14.0, 60.0).moved(Location(Rotation(kp_angle-90, 0, 0)))
        c = c.moved(Location(Vector(cx, kp_mid_y, kp_mid_z)))
        kp_cuts.append(c)
    usb = Box(28.0, 60.0, 16.0).moved(Location(Rotation(kp_angle-90, 0, 0)))
    usb = usb.moved(Location(Vector(w_int/2, kp_mid_y, kp_mid_z)))
    kp_cuts.append(usb)
    p_kp = p_kp - Compound(kp_cuts)

    # VESA: asole 220mm e passacavi
    vesa_angle = math.degrees(math.atan2(scr_u[1], scr_u[0]))
    vesa_cuts = []
    cy_mid = vesa_base[0] + 160.0*scr_u[0]
    cz_mid = vesa_base[1] + 160.0*scr_u[1]
    fc = Cylinder(25.0, 50.0).moved(Location(Rotation(vesa_angle+90, 0, 0)))
    fc = fc.moved(Location(Vector(w_int/2, cy_mid, cz_mid)))
    vesa_cuts.append(fc)
    for t_vesa in [100.0, 125.0, 200.0]:
        vy = vesa_base[0] + t_vesa*scr_u[0]
        vz = vesa_base[1] + t_vesa*scr_u[1]
        v_slot = Box(220.0, 50.0, 6.0).moved(Location(Rotation(vesa_angle+90, 0, 0)))
        v_slot = v_slot.moved(Location(Vector(w_int/2, vy, vz)))
        vesa_cuts.append(v_slot)
    p_vesa = p_vesa - Compound(vesa_cuts)

    # Casse: feritoie
    spk_cuts = []
    for spk_cx in [120.0, w_int - 120.0]:
        for y_off in [-25.0, -15.0, -5.0, 5.0, 15.0, 25.0]:
            slot_y = spk_rear_bot[0] + (55.0 + y_off)*spk_u[0] + th/2*spk_n[0]
            slot_z = spk_rear_bot[1] + (55.0 + y_off)*spk_u[1] + th/2*spk_n[1]
            sl = Box(60.0, 60.0, 4.0).moved(Location(Rotation(spk_angle+90, 0, 0)))
            sl = sl.moved(Location(Vector(spk_cx, slot_y, slot_z)))
            spk_cuts.append(sl)
    vol_hole = Cylinder(4.0, 60.0).moved(Location(Rotation(spk_angle+90, 0, 0)))
    vol_hole = vol_hole.moved(Location(Vector(w_int/2, spk_rear_bot[0] + 55.0*spk_u[0] + th/2*spk_n[0],
                                              spk_rear_bot[1] + 55.0*spk_u[1] + th/2*spk_n[1])))
    spk_cuts.append(vol_hole)
    p_spk = p_spk - Compound(spk_cuts)

    # Tetto: 2 feritoie
    rf_cuts = []
    for t_rf in [50.0, 90.0]:
        ry = rf_p2[0] + t_rf*rf_u[0] - th/2*rf_n[0]
        rz = rf_p2[1] + t_rf*rf_u[1] - th/2*rf_n[1]
        sl = Box(254.0, 60.0, 12.0).moved(Location(Rotation(rf_angle+90, 0, 0)))
        sl = sl.moved(Location(Vector(w_int/2, ry, rz)))
        rf_cuts.append(sl)
    p_roof = p_roof - Compound(rf_cuts)

    # Schienale Superiore: 3 feritoie calore
    rup_cuts = []
    for t_rup in [50.0, 90.0, 130.0]:
        ry = P_out_bot[0] + t_rup*rup_u[0] + th/2*rup_n_in[0]
        rz = P_out_bot[1] + t_rup*rup_u[1] + th/2*rup_n_in[1]
        sl = Box(254.0, 60.0, 12.0).moved(Location(Rotation(rup_angle+90, 0, 0)))
        sl = sl.moved(Location(Vector(w_int/2, ry, rz)))
        rup_cuts.append(sl)
    p_rear_up = p_rear_up - Compound(rup_cuts)

    # Schienale Inferiore: vano sportello (434 x 220mm) + presa IEC a Z=85mm
    door_box = Box(434.0, 50.0, 220.0).moved(Location(Vector(w_int/2, 29.5, 250.0)))
    plug_box = Box(48.0, 50.0, 28.0).moved(Location(Vector(w_int/2, 29.5, 85.0)))
    p_rear_low = p_rear_low - door_box - plug_box

    # Sportello: ventola 120mm + serratura
    fan_hole = Cylinder(60.0, 50.0).moved(Location(Rotation(90, 0, 0))).moved(Location(Vector(w_int/2, 29.5, 250.0)))
    lock_hole = Cylinder(9.5, 50.0).moved(Location(Rotation(90, 0, 0))).moved(Location(Vector(w_int/2 + 185.0, 29.5, 330.0)))
    p_door = p_door - fan_hole - lock_hole

    # Bezel: finestra 16:9
    scr_mid_y = (scr_base[0] + scr_top[0])/2.0
    scr_mid_z = (scr_base[1] + scr_top[1])/2.0
    win_cut = Box(478.0, 30.0, 270.0).moved(Location(Rotation(vesa_angle+90, 0, 0)))
    win_cut = win_cut.moved(Location(Vector(w_int/2, scr_mid_y, scr_mid_z)))
    p_bezel = p_bezel - win_cut

    # Assemblaggio completo dei 16 pezzi
    parts = [
        fiancata_sx, fiancata_dx, tm_sx, tm_dx,
        p_base, p_kp, p_cp, p_vesa, p_spk, p_mq,
        p_roof, p_rear_low, p_rear_up, p_door, p_bezel, lcd
    ]

    print("\n--- Conteggio Solidi di ogni Parte (Target: 1 ciascuna, totale 16) ---")
    all_single_solids = True
    for i, p in enumerate(parts):
        n_solids = len(p.solids())
        lbl = getattr(p, 'label', f'Part_{i+1}')
        print(f"  {i+1:2d}. {lbl}: {n_solids} solido/i")
        if n_solids != 1:
            all_single_solids = False
            print(f"     [ERRORE] La parte {lbl} ha {n_solids} solidi invece di 1!")

    if all_single_solids:
        print(f"\nTOTALE SOLIDI: {len(parts)} su {len(parts)} parti attese.")

    print("\n--- Verifica Automatica Collisioni tra tutte le coppie ---")
    clashes_found = False
    for i in range(len(parts)):
        for j in range(i+1, len(parts)):
            p1, p2 = parts[i], parts[j]
            lbl1 = getattr(p1, 'label', f'Part_{i+1}')
            lbl2 = getattr(p2, 'label', f'Part_{j+1}')
            common = p1.intersect(p2)
            vol = sum(s.volume for s in common.solids()) if hasattr(common, 'solids') else (common.volume if hasattr(common, 'volume') else 0)
            if vol > 1e-3:
                print(f"  * CLASH {lbl1} <-> {lbl2}: {vol:.4f} mm3")
                clashes_found = True

    if not clashes_found:
        print("RISULTATO COLLISIONI: 0.000 mm3 tra tutte le coppie! (Zero Collisioni)")

    print(f"\nEsportazione Compound in STEP: {out_step} ...")
    comp = Compound(parts)
    export_step(comp, out_step)
    file_size = os.path.getsize(out_step)
    print(f"==> FILE STEP GENERATO CON SUCCESSO: {file_size:,} bytes ({out_step})")

if __name__ == "__main__":
    out_file = "/home/paolo/Projects/cabinato/cabinato_arcade_3d.step"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    build_perfect_arcade_model(out_file)
