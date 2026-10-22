# Sito talorynlabs.it — regole

Valgono anche le regole del documento madre `C:\TalorynLabs\CLAUDE.md`.

- Sito statico: solo HTML e CSS, nessun JavaScript (l'unico `<script>` ammesso è il blocco
  `application/ld+json` con i dati dello studio, che non viene eseguito).
- Nessuna risorsa esterna: carattere Montserrat (licenza OFL) in `font/`, icone Phosphor (licenza MIT)
  incluse nel codice delle pagine, immagini in `img/`. Licenze pubblicate in `font/`.
- Identità: colori e immagini da `C:\TalorynLabs\azienda\identita\` (oro #D4AF37, nero #0B0D10).
- Le pagine si generano con `strumenti/costruisci_sito.py`; non modificare a mano gli HTML generati.
- Nessun cookie, nessuna statistica, nessun tracciamento. Lista d'attesa solo via email.
- Ogni affermazione sul prodotto deve corrispondere alla specifica approvata del progetto
  (`progetti/pdf-suite-desktop/docs/specifica-v1.md`). Prezzo: non pubblicarlo finché non è confermato.
- Pubblicazione: GitHub Pages con dominio talorynlabs.it (file `CNAME`). Repository pubblico: mai
  segreti né dati personali nei file.
- Titolare privacy: Taloryn Labs (contatto privacy@ / info@talorynlabs.it). Da aggiornare quando
  nascerà la partita IVA o la società.
