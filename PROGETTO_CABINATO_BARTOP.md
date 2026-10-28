# Progetto Cabinato Arcade Bartop 2P (Configurazione Classic Cabaret)

Progetto esecutivo per cabinato arcade da tavolo a due giocatori con giunzioni a **tenoni e mortase**, ottimizzato per pannelli in **MDF/multistrato da 19 mm** (formato pannelli grezzi $930 \times 720\text{ mm}$) e su misura per monitor **AOC i2269Vwm 21.5" AH-IPS** ($500 \times 310 \times 50\text{ mm}$).

Silhouette **Classic Cabaret**: schienale superiore rastremato in avanti verso il marquee e tetto compatto ridotto a **$142\text{ mm}$** ($\approx 150\text{ mm}$), eliminando qualsiasi sporgenza ingombrante sul retro.

---

## 1. File Attivi del Progetto

| File | Tipo | Descrizione |
| :--- | :--- | :--- |
| **[`cabinato_arcade_cadcraft.dxf`](file:///home/paolo/Projects/cabinato/cabinato_arcade_cadcraft.dxf)** | CAD DXF (R2000) | Disegno esecutivo completo di tutti i pezzi allineati in colonne, con asole e forature. Compatibile CADCraft / AutoCAD / CAM CNC. |
| **[`cabinato_arcade_cadcraft.pdf`](file:///home/paolo/Projects/cabinato/cabinato_arcade_cadcraft.pdf)** | PDF Vettoriale | Tavola tecnica per consultazione e stampa. |
| **[`cabinato_arcade_cadcraft.svg`](file:///home/paolo/Projects/cabinato/cabinato_arcade_cadcraft.svg)** | Vettoriale SVG | Blueprint scalabile per visualizzazione e laser cut. |
| **[`generate_lep1_dxf.py`](file:///home/paolo/Projects/cabinato/generate_lep1_dxf.py)** | Script Python | Generatore parametrico del file DXF esecutivo. |
| **[`generate_3d_step.py`](file:///home/paolo/Projects/cabinato/generate_3d_step.py)** | Script Python | Generatore parametrico del modello 3D STEP solido (16 parti, 0 clash). |
| **[`cabinato_arcade_3d.step`](file:///home/paolo/Projects/cabinato/cabinato_arcade_3d.step)** | Modello 3D STEP | Solido 3D esportato per Onshape e verifiche CAM. |

---

## 2. Specifiche Geometriche e Materiale

- **Spessore Legno:** **19.0 mm** (MDF o multistrato di betulla)
- **Tagli dei Bordi al 100% a 90°:** Tutti i pannelli hanno tagli squadrati a 90° ortogonali alle facce (nessun taglio inclinato/miter/smusso a gradi speciali). Fabbricabili al 100% con banco sega standard o CNC 3 assi.
- **Nastro di Gomma T-Molding (2.0 mm):** Profilo perimetrale in gomma continua protettiva che avvolge tutti gli spigoli esterni delle due fiancate come nei cabinati arcade autentici (Layer `TMOLDING` in ciano nel DXF e solidi dedicati nel modello 3D). Sviluppo: **$1.45\text{ m}$ per fiancata** (**$2.90\text{ m}$ totali**).
- **Tolleranza Asole (Mortase):** **19.2 mm** (fresatura $+0.2\text{ mm}$ per incastro agevole senza gioco)
- **Sporgenza Tenoni Maschio:** **15.0 – 19.0 mm** (a filo della superficie esterna del fianco)
- **Larghezza Interna Utile ($W_{int}$):** **514.0 mm** ($500\text{ mm}$ larghezza schermo AOC $+ 7\text{ mm}$ margine aria per lato)
- **Larghezza Esterna Totale:** **552.0 mm** ($514 + 19 \times 2$)
- **Altezza Massima:** **602.0 mm** (rientra comodamente nel lato da $720\text{ mm}$ del pannello grezzo)
- **Profondità alla Base:** **380.0 mm** | **Profondità Massima Plancia:** **485.0 mm**
- **Profondità del Tetto (Cielo):** **$142.4\text{ mm}$** ($\approx 150\text{ mm}$, compatto Classic Cabaret)

---

## 3. Catena Strutturale Continua Chiusa a 90° (Zero Gap, Zero Miter)

Il mobile è costruito come un solido chiuso auto-portante con bordi rigorosamente a 90°, in cui ogni componente combacia al millimetro con il precedente e il successivo (0 collisioni, 0 fessure):

$$\text{Base } (20, 22) \to (380, 22) \to \text{Frontalino (95.4mm, 90°)} \to \text{[sotto plancia a } Z=131.5]$$
$$\text{Plancia } (268, 175) \to (470, 147.5) \text{ [aggetto 25mm ergonomico]} \to \text{Bezel} \to (150, 470)$$
$$\text{Casse Audio (114.4mm, 90°)} \to \text{Marquee (80.8mm)} \to \text{Tetto (142.4mm, 90°)}$$
$$\to \text{Schienale Superiore Spiovente (163.6mm, 90°)} \to \text{Schienale Inferiore Verticale (Z=41..380)}$$

Nessun elemento fluttua nel vuoto:
1. **Frontalino Kickplate ($95.4\text{ mm}$):** Con taglio a 90°, la testa del frontalino chiude a filo sotto la plancia. L'aggetto frontale della plancia copre interamente lo spigolo a 90° senza giunzioni a vista.
2. **Pannello Casse Audio ($114.4\text{ mm}$):** Con taglio a 90°, tocca a filo contro la faccia interna del marquee chiudendo ermeticamente senza buchi. Spazio abbondante per altoparlanti da $3''$ / $4''$.
3. **Tetto Cielo ($142.4\text{ mm}$):** Con taglio a 90°, poggia direttamente sulla sommità dello schienale superiore spiovente coprendo interamente la sommità della cabina.
4. **Schienale Posteriore a Doppio Settore:**
   - **Inferiore Verticale ($514 \times 339\text{ mm}$):** da quota $Z=41$ a $Z=380\text{ mm}$, alloggia la presa IEC C14 alzata a $Z=85$ e il vano per lo sportello di manutenzione ($434 \times 220\text{ mm}$).
   - **Superiore Spiovente ($514 \times 163.6\text{ mm}$):** da quota $Z=380\text{ mm}$ piega in avanti con angolo $68.75^\circ$ fino a battuta sotto il tetto, chiudendo il volume posteriore con 3 feritoie di evacuazione calore.
5. **Nastro di Gomma T-Molding (2.0 mm):** Corre lungo tutto il perimetro curvo delle due fiancate proteggendo gli spigoli da urti e usura.

---

## 4. Caratteristiche dei Componenti (Colonna per Colonna)

### Colonna 1: Fiancata Laterale (SX e DX) - $602 \times 485\text{ mm}$
- **Profilo Classic Cabaret**: Silhouette a "C-curve" continua con musetto frontale avanzato a protezione della plancia e rastremazione posteriore alta verso il marquee.
- **Incasso Schermo**: Il monitor da 21.5" è incassato all'interno, protetto dai riflessi di luce laterali.
- **Guancia Plancia**: Musetto avanzato a $X = 485\text{ mm}$ che sale a protezione dei tasti e delle mani.
- **Senza Foro Flipper**: Rimosso su specifica utente.
- **12 Mortase Femmina**: Tutte ortogonali e ricavate con margine di legno pieno $\ge 20-32\text{ mm}$ su tutti i bordi (incluso il doppio ancoraggio dello schienale inferiore con mortasa bassa $Z=70..130$ e mortasa alta $Z=290..350$).

### Colonna 2: Plancia 2P, Frontalino e Base
- **Plancia Comandi 2P ($514 \times 204\text{ mm}$)**:
  - 4 tenoni maschio da $40\text{ mm}$ (a quota $t=30..70$ e $t=105..145\text{ mm}$).
  - **Ergonomia Giocatori Verificata:** Sia per il Giocatore 1 (a sinistra) che per il Giocatore 2 (a destra), la **leva joystick è a SINISTRA** e i **6 tasti azione sono a DESTRA**, rispettando rigorosamente lo standard arcade mondiale (Sanwa).
  - **Orientamento Corretto:** Bordo posteriore ($t=0$) a contatto con il bezel monitor, bordo anteriore ($t=204\text{ mm}$) rivolto verso il giocatore.
  - **Tasti Admin (Start & Coin):** Posizionati in alto ($t=36..42\text{ mm}$, zona bezel), ben lontani dalle mani durante il gioco.
  - **Joystick & Tasti Azione:** 2 Joystick Sanwa JLF ($\varnothing 30\text{ mm}$ + 4 fori vite) e $2 \times 6$ tasti azione curvi ($\varnothing 28\text{ mm}$) posizionati al centro nel vano cavo ($t=75..128\text{ mm}$).
  - **Zero Clash con il Frontalino:** Il frontalino chiude a quota $t=147.1..164.8\text{ mm}$. La distanza minima tra il foro più basso dei tasti e il frontalino è di ben **$19.1\text{ mm}$** di legno pieno. Nessun foro si trova sopra o vicino al frontalino!
  - **Zona Appoggio Polsi:** Gli ultimi $70\text{ mm}$ verso il giocatore ($t=134..204\text{ mm}$) sono completamente puliti e privi di fori, con un comodo aggetto di $39\text{ mm}$ oltre il frontalino per poggiare i polsi.
- **Frontalino Kickplate ($514 \times 95.4\text{ mm}$, Taglio 90°)**:
  - 2 tenoni maschio da $50\text{ mm}$ centrati.
  - Chiude subito sotto la plancia ($t=147.1..164.8\text{ mm}$ dal bordo posteriore), lasciando l'intero vano retrostante libero per il cablaggio.
  - 2 fori Coin supplementari frontali ($\varnothing 28\text{ mm}$) e vano centrale per doppia porta USB.
- **Base Inferiore ($514 \times 360\text{ mm}$)**:
  - 4 tenoni maschio da $70\text{ mm}$.
  - 3 feritoie di ventilazione per ingresso aria fresca dal basso.
  - 4 fori per piedini in gomma ($\varnothing 12\text{ mm}$).

### Colonna 3: Bezel, Traversa VESA, Casse Audio e Marquee
- **Cornice / Bezel Monitor ($514 \times 318\text{ mm}$)**: Finestra utile $478 \times 270\text{ mm}$ (matrice attiva 16:9 AOC).
- **Traversa VESA ($514 \times 300\text{ mm}$)**:
  - 4 tenoni maschio da $45\text{ mm}$, inclinazione $68.0^\circ$, recesso $56\text{ mm}$ dal vetro.
  - **Doppie asole orizzontali scorrevoli ($220\text{ mm}$)**: permettono di traslare lo schermo lateralmente per centrarlo al millimetro. Forature VESA 75 e VESA 100.
  - Vano passacavi centrale $\varnothing 50\text{ mm}$ e asola inferiore per connettori orizzontali AOC (HDMI / alimentazione).
- **Pannello Casse Audio Zero-Gap a 90° ($514 \times 114.4\text{ mm}$)**:
  - Chiusura continua da cima schermo a fondo marquee: zero buchi o fessure visibili.
  - Taglio a 90° frontale a battuta diretta sulla faccia interna del marquee.
  - Spazio ampio per altoparlanti da $3''$ o $4''$.
  - 2 tenoni maschio da $60\text{ mm}$ centrati su entrambi i lati.
  - Griglie audio a 6 feritoie orizzontali graduate fresate direttamente nel legno.
  - Foro centrale per regolatore volume / presa cuffie da 3.5 mm.
- **Insegna Marquee Superiore ($514 \times 80.8\text{ mm}$)**: Compatto e proporzionato per un look classico Cabaret.

### Colonna 4: Tetto e Doppio Schienale
- **Tetto Superiore Cielo a 90° ($514 \times 142.4\text{ mm}$)**:
  - Tetto compatto Classic Cabaret ($\approx 150\text{ mm}$).
  - 2 feritoie orizzontali di espulsione calore naturale, 2 tenoni da $75\text{ mm}$.
- **Schienale Inferiore Verticale ($514 \times 339\text{ mm}$)**:
  - Da quota $Z=41$ a $Z=380\text{ mm}$.
  - **4 tenoni maschio da $60\text{ mm}$** (2 per lato: Tenone Basso a $Z=70..130\text{ mm}$, Tenone Alto a $Z=290..350\text{ mm}$) per un solido doppio ancoraggio strutturale alle fiancate che azzera qualsiasi oscillazione del telaio posteriore.
  - Presa 220V IEC C14 con interruttore e fusibile **alzata a $Z=85\text{ mm}$** ($44\text{ mm}$ sopra il fondo), vano interno retrostante completamente libero.
  - Vano centrale per sportello di manutenzione ($434 \times 220\text{ mm}$).
- **Schienale Superiore Spiovente ($514 \times 163.6\text{ mm}$)**:
  - Inclinato in avanti a $68.75^\circ$.
  - 2 tenoni maschio da $90\text{ mm}$.
  - 3 feritoie orizzontali per dissipazione calore naturale dei circuiti e dell'amplificatore.

### Colonna 5: Sportello di Manutenzione
- **Sportello Posteriore Indipendente ($430 \times 216\text{ mm}$)**:
  - Apertura centrale per ventola silenziosa da 120 mm con 4 fori viti.
  - Foro per serratura a cilindro con chiave ($\varnothing 19\text{ mm}$).
  - Incavi per cerniere a libro sul lato sinistro per facile apertura.

---

## 5. Verifica del Montaggio 3D su Onshape

Il modello 3D parametrico aggiornato è disponibile online su Onshape per ispezione visiva e dimensionale:

- **Link Diretto Documento:** [Onshape - cabinato_arcade_3d](https://cad.onshape.com/documents/af3b4b497b0a69e48a71c2d8/w/fdb592fbbd6be150031a8324/e/2d3ad09827e7d67b9e78437e)
- **Parti Riconosciute nel Modello:** esattamente **16 solidi indipendenti**:
  1. `Fiancata_Sinistra`
  2. `Fiancata_Destra`
  3. `T_Molding_Fiancata_Sinistra`
  4. `T_Molding_Fiancata_Destra`
  5. `Base_Inferiore`
  6. `Frontalino_Kickplate`
  7. `Plancia_Comandi_2P`
  8. `Traversa_Supporto_VESA`
  9. `Pannello_Casse_Audio`
  10. `Insegna_Marquee`
  11. `Tetto_Superiore`
  12. `Schienale_Inferiore_Verticale`
  13. `Schienale_Superiore_Spiovente`
  14. `Sportello_Posteriore`
  15. `Bezel_Monitor`
  16. `Schermo_LCD_AOC`
- **Volume di Collisione:** **$0.000\text{ mm}^3$** (zero collisioni matematiche).
