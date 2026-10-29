"""Genera il sito statico di Taloryn Labs (HTML + CSS, nessun JavaScript).

Uso (dalla cartella del sito): python3 strumenti/costruisci_sito.py . <cartella assets di @phosphor-icons/core 2.1.1>
Ogni pagina condivide testata e piede; le icone Phosphor (licenza MIT) sono incluse nel codice.
"""
import json, re, sys
from pathlib import Path

OUT = Path(sys.argv[1]); PH = Path(sys.argv[2])
DOMINIO = "https://talorynlabs.it"
EMAIL = "info@talorynlabs.it"
AGGIORNATO = "29 ottobre 2026"
ANNO = "2026"


def ico(nome, peso="light"):
    f = PH / peso / (f"{nome}.svg" if peso == "regular" else f"{nome}-{peso}.svg")
    svg = f.read_text()
    svg = svg.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg aria-hidden="true" focusable="false"')
    return svg


ATTESA = ("mailto:info@talorynlabs.it?subject=Lista%20d%27attesa%20Riserbo"
          "&amp;body=Vorrei%20essere%20avvisato%20quando%20Riserbo%20sar%C3%A0%20disponibile."
          "%0A%0ATipo%20di%20studio%20(facoltativo)%3A%20")

MENU = [("/", "Studio"), ("/riserbo.html", "Riserbo"), ("/sicurezza.html", "Sicurezza"),
        ("/guide/", "Guide"), ("/contatti.html", "Contatti")]


def testata(attivo):
    voci = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == attivo else ""}>{t}</a>' for h, t in MENU)
    return f'''<a class="salta" href="#contenuto">Vai al contenuto</a>
<header class="testata">
  <div class="contenitore">
    <a class="logo" href="/" aria-label="Taloryn Labs, pagina principale"><img src="/img/logo-480.webp" srcset="/img/logo-240.webp 240w, /img/logo-480.webp 480w" sizes="168px" width="168" height="52" alt="Taloryn Labs"></a>
    <nav class="menu" aria-label="Principale">{voci}<a class="pulsante-menu" href="/contatti.html#lista-attesa">Lista d'attesa</a></nav>
  </div>
</header>'''


PIEDE = f'''<footer class="piede">
  <div class="contenitore">
    <div class="griglia">
      <div>
        <img src="/img/logo-480.webp" width="176" height="54" alt="Taloryn Labs">
        <p>Software per studi professionali. Regole chiare, dati protetti.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h2>Studio</h2>
        <ul><li><a href="/">Chi siamo</a></li><li><a href="/sicurezza.html">Sicurezza</a></li><li><a href="/contatti.html">Contatti</a></li></ul>
      </div>
      <div>
        <h2>Prodotto</h2>
        <ul><li><a href="/riserbo.html">Riserbo</a></li><li><a href="/contatti.html#lista-attesa">Lista d'attesa</a></li><li><a href="/guide/">Guide</a></li></ul>
      </div>
      <div>
        <h2>Note legali</h2>
        <ul><li><a href="/privacy.html">Informativa privacy</a></li><li><a href="/termini.html">Condizioni d'uso</a></li></ul>
      </div>
    </div>
    <div class="fondo">
      <span>© {ANNO} Taloryn Labs - Tutti i diritti riservati.</span>
      <span>Questo sito non usa cookie né strumenti di tracciamento.</span>
    </div>
  </div>
</footer>'''

FASCIA = f'''<section class="fascia" aria-labelledby="t-fascia">
  <div class="contenitore">
    <h2 id="t-fascia">Vuoi sapere quando Riserbo sarà pronto?</h2>
    <p>Scrivici da un indirizzo del tuo studio. Ti avvisiamo una sola volta, quando il programma sarà disponibile.</p>
    <div class="azioni"><a class="pulsante" href="{ATTESA}">{ico("envelope-simple", "regular")}Entra nella lista d'attesa</a></div>
  </div>
</section>'''


def pagina(percorso, titolo, descrizione, attivo, corpo, fascia=True, extra_head=""):
    url = DOMINIO + ("/" + percorso if percorso != "index.html" else "/")
    url = url.replace("/index.html", "/")
    html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descrizione}">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#0B0D10">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/img/icona-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/font/montserrat-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/font/montserrat-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/stile.css">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Taloryn Labs">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/img/anteprima-condivisione.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{extra_head}</head>
<body>
{testata(attivo)}
<main id="contenuto">
{corpo}
{FASCIA if fascia else ""}
</main>
{PIEDE}
</body>
</html>
'''
    dest = OUT / percorso
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return url


ORG = json.dumps({
    "@context": "https://schema.org", "@type": "Organization", "name": "Taloryn Labs",
    "url": DOMINIO + "/", "logo": DOMINIO + "/img/icona-512.png", "email": EMAIL,
    "description": "Software per studi professionali italiani: regole verificabili, elaborazione sul computer dell'utente."},
    ensure_ascii=False)

# ------------------------------------------------------------------ STUDIO (home)
home = f'''<section class="apertura" aria-labelledby="t-apertura">
  <div class="contenitore">
    <div>
      <div class="occhiello">Software per studi professionali</div>
      <h1 id="t-apertura">Software che non sbaglia in silenzio.</h1>
      <p class="introduzione" style="margin-top:24px">Taloryn Labs crea programmi per commercialisti, avvocati, consulenti del lavoro, amministratori di condominio e agenzie. Seguono regole scritte e verificabili, lavorano sul tuo computer e, se incontrano un caso che non conoscono, si fermano e te lo dicono.</p>
      <div class="azioni">
        <a class="pulsante" href="/riserbo.html">Scopri Riserbo{ico("arrow-right", "regular")}</a>
        <a class="secondario" href="/contatti.html#lista-attesa">Entra nella lista d'attesa</a>
      </div>
      <p class="motto">Regole chiare. Dati protetti.</p>
    </div>
    <div class="pannello">
      <img src="/img/pannello-920.webp" srcset="/img/pannello-460.webp 460w, /img/pannello-920.webp 920w" sizes="(max-width: 980px) 300px, 400px" width="400" height="657" alt="Il simbolo di Taloryn Labs: una T d'oro con una vena luminosa e una sfera alla base, sopra la scritta Taloryn Labs" fetchpriority="high">
    </div>
  </div>
</section>

<section class="sezione" aria-labelledby="t-principi">
  <div class="contenitore">
    <div class="testa-sezione">
      <div><div class="occhiello">Come lavoriamo</div><h2 id="t-principi">Quattro promesse che puoi controllare.</h2></div>
      <p>Chi lavora con i dati dei clienti non può fidarsi di un programma che "più o meno" funziona. Per questo ogni nostro prodotto rispetta queste regole, e le scriviamo qui perché tu possa verificarle.</p>
    </div>
    <div class="schede">
      <div class="scheda"><div class="icona">{ico("scales")}</div><h3>Regole, non indovinelli</h3><p>Il cuore dei nostri programmi segue regole scritte e verificabili: a parità di documento, stesso risultato. L'intelligenza artificiale, se c'è, è solo un aiuto facoltativo e non decide mai da sola.</p></div>
      <div class="scheda"><div class="icona">{ico("cloud-slash")}</div><h3>Sul tuo computer</h3><p>I documenti restano nel tuo studio. Niente cloud, niente account obbligatori, niente pubblicità, nessuna vendita di dati.</p></div>
      <div class="scheda"><div class="icona">{ico("tag")}</div><h3>Prezzo chiaro</h3><p>Il prezzo di ogni prodotto è pubblicato sul sito, uguale per tutti. Nessun costo nascosto e nessuna trattativa per scoprirlo.</p></div>
      <div class="scheda"><div class="icona">{ico("chat-text")}</div><h3>Assistenza per iscritto</h3><p>Rispondiamo via email, con risposte precise che restano agli atti e che puoi rileggere quando vuoi.</p></div>
    </div>
  </div>
</section>

<section class="sezione scura" aria-labelledby="t-prodotto">
  <div class="contenitore">
    <div class="prodotto">
      <div class="testo-prodotto">
        <div class="occhiello">Il primo prodotto</div>
        <h2 id="t-prodotto">Riserbo</h2>
        <p class="corpo" style="margin-top:16px">Toglie davvero codici fiscali, IBAN e nomi da PDF e file Word, sul tuo computer e senza internet. Poi rilegge il file da zero e controlla che non ne resti traccia.</p>
        <ul class="elenco-segni">
          <li>{ico("check-circle")}<span>Riconosce codice fiscale, partita IVA e IBAN anche con il loro carattere di controllo.</span></li>
          <li>{ico("check-circle")}<span>Rimuove il dato dal file, non lo copre soltanto: anche da metadati, commenti e revisioni.</span></li>
          <li>{ico("check-circle")}<span>Se dopo la verifica un dato è ancora leggibile, il file non viene salvato.</span></li>
        </ul>
        <div class="stato"><i></i>In sviluppo · per Windows 10 e 11</div>
        <div class="azioni"><a class="pulsante" href="/riserbo.html">Come funziona{ico("arrow-right", "regular")}</a></div>
      </div>
      <div class="figura-prodotto">
        <figure class="documento" aria-label="Esempio di documento oscurato">
          <div aria-hidden="true">
            <div class="intestazione-doc">Dichiarazione sostitutiva</div>
            <p>La sottoscritta <span class="dato">Laura Bianchi</span>, codice fiscale <span class="dato">BNCLRA82M45G388D</span>, residente in <span class="dubbio">via dei Mille 14</span>, chiede l'accredito sul conto IBAN <span class="dato">IT60 X054 2811 1010 0000 0123 456</span>.</p>
            <div class="esito">
              <span><i class="segno nero"></i>3 dati rimossi dal file</span>
              <span><i class="segno giallo"></i>1 indirizzo da controllare a occhio</span>
              <span><i class="segno verde"></i>Verifica superata</span>
            </div>
          </div>
        </figure>
      </div>
    </div>
  </div>
</section>

<section class="sezione" aria-labelledby="t-nome">
  <div class="contenitore racconto">
    <div class="marchio-grande"><img src="/img/marchio-600.webp" srcset="/img/marchio-300.webp 300w, /img/marchio-600.webp 600w" sizes="300px" width="300" height="352"  alt="La T d'oro di Taloryn Labs" loading="lazy" decoding="async"></div>
    <div>
      <div class="occhiello">Il nome</div>
      <h2 id="t-nome">Da Talos, il custode di bronzo.</h2>
      <div class="corpo" style="margin-top:20px">
        <p>Nel mito greco Talos era il gigante di bronzo che sorvegliava Creta. Secondo un antico racconto portava di villaggio in villaggio le leggi dell'isola, incise su tavole di bronzo, perché fossero rispettate da tutti allo stesso modo.</p>
        <p>Nel suo corpo scorreva un'unica vena, chiusa da un chiodo. La nostra T d'oro viene da lì: la traversa come le tavole delle leggi, la vena luminosa al centro, la sfera alla base.</p>
      </div>
      <blockquote>Un custode affidabile non improvvisa: applica la regola, e quando la regola non basta, chiama qualcuno.</blockquote>
    </div>
  </div>
</section>

<section class="sezione scura" aria-labelledby="t-per-chi">
  <div class="contenitore due-colonne">
    <div><div class="occhiello">Per chi</div><h2 id="t-per-chi">Per chi tratta ogni giorno i dati degli altri.</h2></div>
    <div>
      <p class="corpo">Lavoriamo solo per studi e imprese, con licenza per postazione. Conosciamo i documenti che girano in uno studio italiano: dichiarazioni, buste paga, atti, verbali, contratti.</p>
      <div class="professioni">
        <span>{ico("calculator")}Commercialisti</span>
        <span>{ico("scales")}Avvocati</span>
        <span>{ico("identification-card")}Consulenti del lavoro</span>
        <span>{ico("buildings")}Amministratori di condominio</span>
        <span>{ico("briefcase")}Agenzie</span>
      </div>
    </div>
  </div>
</section>'''
pagina("index.html", "Taloryn Labs — software per studi professionali",
       "Taloryn Labs crea software per studi professionali italiani: regole verificabili, dati che restano sul tuo computer, prezzo chiaro e assistenza per iscritto.",
       "/", home, extra_head=f'<script type="application/ld+json">{ORG}</script>\n')

# ------------------------------------------------------------------ RISERBO
pdf = f'''<section class="testa-pagina con-figura" aria-labelledby="t-pdf">
  <div class="contenitore">
    <div>
      <div class="occhiello">Riserbo</div>
      <h1 id="t-pdf">Documenti dei clienti, condivisi senza i loro dati.</h1>
      <p class="introduzione" style="margin-top:24px">Riserbo toglie codici fiscali, IBAN e nomi da PDF e file Word in italiano. Lavora sul tuo computer, senza internet, e prima di salvare controlla che nel file non ne resti traccia.</p>
      <div class="stato"><i></i>In sviluppo · per Windows 10 e 11</div>
      <div class="azioni">
        <a class="pulsante" href="{ATTESA}">{ico("envelope-simple", "regular")}Entra nella lista d'attesa</a>
        <a class="secondario" href="#come-funziona">Come funziona</a>
      </div>
    </div>
    <figure class="documento" aria-labelledby="doc-descrizione">
      <p id="doc-descrizione" class="visivamente-nascosto">Esempio: in una dichiarazione il nome, il codice fiscale, il comune di nascita e l'IBAN vengono oscurati; l'indirizzo viene evidenziato in giallo per un controllo a occhio; la verifica finale conferma che nel file non resta nessun dato oscurato.</p>
      <div aria-hidden="true">
        <div class="intestazione-doc">Dichiarazione sostitutiva di certificazione</div>
        <p>La sottoscritta <span class="dato">Laura Bianchi</span>, codice fiscale <span class="dato">BNCLRA82M45G388D</span>, nata a <span class="dato">Pavia</span>, residente in <span class="dubbio">via dei Mille 14</span>, dichiara di essere titolare del conto corrente</p>
        <p>IBAN <span class="dato">IT60 X054 2811 1010 0000 0123 456</span> presso cui chiede l'accredito delle somme spettanti.</p>
        <div class="esito">
          <span><i class="segno nero"></i>4 dati rimossi dal file</span>
          <span><i class="segno giallo"></i>1 indirizzo da controllare a occhio</span>
          <span><i class="segno verde"></i>Verifica: nessun dato rimosso è ancora leggibile nel file</span>
        </div>
      </div>
    </figure>
  </div>
</section>

<section class="sezione" aria-labelledby="t-coprire">
  <div class="contenitore due-colonne">
    <div>
      <div class="occhiello">Il problema</div>
      <h2 id="t-coprire">Coprire non è cancellare.</h2>
    </div>
    <div class="corpo">
      <p>Un rettangolo nero disegnato sopra un PDF nasconde il testo allo sguardo, ma spesso il testo resta nel file: basta selezionarlo e copiarlo. Nei file Word succede lo stesso con commenti, proprietà del documento e cronologia delle revisioni.</p>
      <p>Il documento sembra pulito, ma chi lo riceve, un collega, un ufficio o uno strumento di intelligenza artificiale, può ancora leggere quei dati. <a href="/guide/coprire-non-e-cancellare.html">Perché succede</a>.</p>
    </div>
  </div>
  <div class="contenitore">
    <div class="confronto">
      <div class="loro"><h3>{ico("prohibit")}Strumenti di copertura</h3><p>Disegnano sopra il dato. Il file sembra pulito, ma il contenuto originale può essere ancora dentro.</p></div>
      <div class="nostro"><h3>{ico("seal-check")}Riserbo</h3><p>Toglie il dato dal file, poi rilegge il risultato da zero. Se trova ancora qualcosa, non salva.</p></div>
    </div>
  </div>
</section>

<section class="sezione scura" id="come-funziona" aria-labelledby="t-come">
  <div class="contenitore">
    <div class="testa-sezione">
      <div><div class="occhiello">Come funziona</div><h2 id="t-come">Quattro passaggi, l'ultima parola è tua.</h2></div>
      <p>Il programma propone, tu decidi. Niente viene tolto o lasciato senza che tu lo veda.</p>
    </div>
    <ol class="passi">
      <li><h3>Apri il documento</h3><p>Un PDF, anche scansionato, una foto di un documento o un file Word (.docx) in italiano. Il file non lascia mai il tuo computer.</p></li>
      <li><h3>Il programma trova i dati</h3><p>Codici fiscali, partite IVA, IBAN, email e telefoni in automatico. Nomi e cognomi li indichi tu, e vengono cercate anche le varianti.</p></li>
      <li><h3>Controlli pagina per pagina</h3><p>Vedi ogni pagina con le zone proposte. Indirizzi, date di nascita e riferimenti indiretti sono segnalati in giallo. Approvi, togli o aggiungi.</p></li>
      <li><h3>Rimozione e verifica</h3><p>Il dato viene tolto dal file. Il risultato viene riletto da zero: se un dato è ancora presente, il salvataggio si blocca.</p></li>
    </ol>
  </div>
</section>

<section class="sezione" aria-labelledby="t-trova">
  <div class="contenitore">
    <div class="testa-sezione">
      <div><div class="occhiello">Che cosa trova</div><h2 id="t-trova">Ogni tipo di dato ha la sua regola.</h2></div>
      <p>Dove esiste un controllo matematico lo usiamo: un codice fiscale con il carattere di controllo sbagliato non è un codice fiscale. <a href="/guide/codici-di-controllo.html">Come funziona il controllo</a>.</p>
    </div>
    <div class="contorno-tabella">
      <table class="tabella">
        <thead><tr><th scope="col">Dato</th><th scope="col">Come viene riconosciuto</th><th scope="col">Cosa succede</th></tr></thead>
        <tbody>
          <tr><td>Codice fiscale</td><td>Struttura e carattere di controllo, comprese le omocodie.</td><td><span class="etichetta oro">Proposto per la rimozione</span></td></tr>
          <tr><td>Partita IVA</td><td>Undici cifre e cifra di controllo.</td><td><span class="etichetta oro">Proposto per la rimozione</span></td></tr>
          <tr><td>IBAN italiano</td><td>Struttura e codice di controllo internazionale.</td><td><span class="etichetta oro">Proposto per la rimozione</span></td></tr>
          <tr><td>Email e telefono</td><td>Forma dell'indirizzo email e dei numeri di telefono.</td><td><span class="etichetta oro">Proposto per la rimozione</span></td></tr>
          <tr><td>Nomi e cognomi</td><td>Quelli che indichi tu, con le varianti: maiuscole, ordine invertito, iniziali.</td><td><span class="etichetta oro">Proposto per la rimozione</span></td></tr>
          <tr><td>Riferimenti indiretti</td><td>Indirizzi, date di nascita, frasi come "il figlio del mio cliente".</td><td><span class="etichetta giallo">Segnalato in giallo, decidi tu</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="sezione scura" aria-labelledby="t-toglie">
  <div class="contenitore due-colonne">
    <div>
      <div class="occhiello">Che cosa toglie</div>
      <h2 id="t-toglie">Anche quello che non si vede.</h2>
      <p class="corpo" style="margin-top:18px">Un file contiene molto più di quello che appare sulla pagina. Riserbo pulisce anche le parti nascoste, e alla fine ti consegna un rapporto.</p>
    </div>
    <ul class="elenco-segni">
      <li>{ico("eraser")}<span><strong>Il testo oscurato</strong>, che viene rimosso dal file e non solo coperto.</span></li>
      <li>{ico("file-magnifying-glass")}<span><strong>I metadati</strong>: autore, titolo e altre proprietà del documento.</span></li>
      <li>{ico("chat-text")}<span><strong>I commenti</strong> e le note.</span></li>
      <li>{ico("file-pdf")}<span><strong>Gli allegati</strong> contenuti nel file.</span></li>
      <li>{ico("file-doc")}<span><strong>La cronologia delle revisioni</strong> dei file Word.</span></li>
      <li>{ico("list-checks")}<span><strong>Il rapporto finale</strong>: cosa è stato tolto, pagina per pagina, senza riportare i dati.</span></li>
    </ul>
  </div>
</section>

<section class="sezione" aria-labelledby="t-limiti">
  <div class="contenitore due-colonne">
    <div>
      <div class="occhiello">Con onestà</div>
      <h2 id="t-limiti">Cosa non fa, per ora.</h2>
      <p class="corpo" style="margin-top:18px">La prima versione fa una cosa sola e deve farla bene. Preferiamo dirlo prima.</p>
    </div>
    <ul class="elenco-segni">
      <li>{ico("warning")}<span>Non legge la scrittura a mano.</span></li>
      <li>{ico("warning")}<span>Lavora sui documenti in italiano, solo su Windows.</span></li>
      <li>{ico("warning")}<span>Elabora un documento alla volta, non intere cartelle.</span></li>
      <li>{ico("warning")}<span>Non usa l'intelligenza artificiale per decidere cosa togliere.</span></li>
    </ul>
  </div>
</section>

<section class="sezione scura" aria-labelledby="t-requisiti">
  <div class="contenitore">
    <div class="testa-sezione">
      <div><div class="occhiello">Dettagli</div><h2 id="t-requisiti">Requisiti, qualità e prezzo.</h2></div>
      <p>Numeri che pubblicheremo così come sono, anche quando non saranno perfetti.</p>
    </div>
    <div class="schede">
      <div class="scheda"><div class="icona">{ico("desktop-tower")}</div><h3>Requisiti</h3><p>Windows 10 o 11 a 64 bit. Funziona senza connessione a internet.</p></div>
      <div class="scheda"><div class="icona">{ico("list-checks")}</div><h3>Qualità misurata</h3><p>Lo proviamo su una raccolta di documenti inventati, con dati finti. Pubblicheremo quanti dati trova e quanti falsi allarmi dà. L'obiettivo per codici e IBAN: nessun dato mancato.</p></div>
      <div class="scheda"><div class="icona">{ico("monitor")}</div><h3>Velocità</h3><p>L'obiettivo è analizzare un documento di 50 pagine in meno di 30 secondi su un normale PC d'ufficio. Pubblicheremo la misura reale.</p></div>
      <div class="scheda"><div class="icona">{ico("tag")}</div><h3>Prezzo</h3><p>Licenza annuale per postazione, con prova gratuita. Il prezzo sarà pubblicato su questa pagina prima dell'uscita.</p></div>
    </div>
  </div>
</section>

<section class="sezione" aria-labelledby="t-domande">
  <div class="contenitore due-colonne">
    <div><div class="occhiello">Domande</div><h2 id="t-domande">Domande frequenti.</h2></div>
    <div class="domande">
      <details><summary>I miei documenti arrivano a voi?</summary><p>No. Il programma lavora solo sul tuo computer e non si collega a internet. I documenti che apri non lasciano mai il tuo studio.</p></details>
      <details><summary>Funziona con i documenti scansionati?</summary><p>Sì. Il testo delle scansioni e delle foto viene riconosciuto sul tuo computer, senza internet. Le parole lette con poca sicurezza sono segnalate in giallo, e l'oscuramento cancella davvero l'immagine nella zona, non la copre. La qualità dipende dalla scansione: pubblicheremo i risultati delle prove separati da quelli dei documenti con testo.</p></details>
      <details><summary>Usa l'intelligenza artificiale?</summary><p>No. Ogni dato viene riconosciuto con regole precise e, dove esiste, con il controllo matematico. Così lo stesso documento dà sempre lo stesso risultato, e puoi capire perché.</p></details>
      <details><summary>E se il programma sbaglia?</summary><p>Per questo c'è la revisione pagina per pagina: vedi tutto quello che viene proposto e puoi togliere o aggiungere. Alla fine il file viene riletto: se un dato oscurato è ancora presente, il salvataggio si blocca.</p></details>
      <details><summary>Quando esce?</summary><p>Non abbiamo ancora una data e non vogliamo inventarla. Iscriviti alla lista d'attesa: ti scriviamo una sola volta, quando sarà disponibile.</p></details>
    </div>
  </div>
</section>'''
pagina("riserbo.html", "Riserbo — oscuramento vero di PDF e Word | Taloryn Labs",
       "Riserbo rimuove davvero codici fiscali, IBAN e nomi dai PDF e dai file Word, sul tuo computer e senza internet, e verifica che non ne resti traccia.",
       "/riserbo.html", pdf)

# ------------------------------------------------------------------ SICUREZZA
sic = f'''<section class="testa-pagina" aria-labelledby="t-sic">
  <div class="contenitore">
    <div class="occhiello">Sicurezza</div>
    <h1 id="t-sic">I tuoi dati restano dove sono.</h1>
    <p class="introduzione" style="margin-top:24px">Il modo più sicuro di proteggere un dato è non spostarlo. Per questo i nostri programmi lavorano sul tuo computer e il nostro sito non raccoglie niente di te.</p>
  </div>
</section>

<section class="sezione" aria-labelledby="t-programma">
  <div class="contenitore">
    <div class="testa-sezione">
      <div><div class="occhiello">Il programma</div><h2 id="t-programma">Che cosa fa Riserbo con i tuoi file.</h2></div>
      <p>Queste regole fanno parte della specifica del prodotto, non sono promesse di marketing.</p>
    </div>
    <div class="schede">
      <div class="scheda"><div class="icona">{ico("wifi-slash")}</div><h3>Nessuna connessione</h3><p>Il programma non si collega a internet: niente invio di dati, niente statistiche di utilizzo, niente aggiornamenti automatici silenziosi.</p></div>
      <div class="scheda"><div class="icona">{ico("lock-key")}</div><h3>Tutto in locale</h3><p>I documenti vengono aperti, analizzati e salvati sul tuo computer. Non esiste una copia sui nostri sistemi.</p></div>
      <div class="scheda"><div class="icona">{ico("seal-check")}</div><h3>Verifica che blocca</h3><p>Il file finale viene riletto da zero. Se un dato oscurato è ancora presente, il salvataggio non avviene.</p></div>
      <div class="scheda"><div class="icona">{ico("list-checks")}</div><h3>Rapporto senza dati</h3><p>Il riepilogo dice cosa è stato tolto e dove, ma non riporta i dati: puoi conservarlo senza creare una nuova copia delle informazioni.</p></div>
      <div class="scheda"><div class="icona">{ico("fingerprint")}</div><h3>Registro che non si ritocca</h3><p>Ogni operazione è scritta in un registro in cui ogni riga contiene l'impronta della precedente: una modifica si scopre. Se vuoi una prova davanti a terzi, puoi apporre una marca temporale sulle impronte, senza inviare il documento.</p></div>
    </div>
  </div>
</section>

<section class="sezione scura" aria-labelledby="t-metodo">
  <div class="contenitore due-colonne">
    <div><div class="occhiello">Il metodo</div><h2 id="t-metodo">Regole verificabili, casi dubbi in evidenza.</h2></div>
    <div class="corpo">
      <p>Il nucleo dei nostri programmi è <strong>deterministico</strong>: segue regole scritte, e lo stesso documento dà sempre lo stesso risultato. Così un errore si può riprodurre, capire e correggere.</p>
      <p>Quando il programma incontra qualcosa che non sa classificare con certezza, non tira a indovinare: <strong>lo segnala</strong> e lascia a te la decisione. È il motivo per cui i riferimenti indiretti, come indirizzi e date di nascita, sono evidenziati in giallo.</p>
      <p>Nessun programma sostituisce la tua attenzione. Per questo la revisione pagina per pagina fa parte del lavoro, e non è un passaggio facoltativo.</p>
    </div>
  </div>
</section>

<section class="sezione" aria-labelledby="t-sviluppo">
  <div class="contenitore due-colonne">
    <div><div class="occhiello">Come sviluppiamo</div><h2 id="t-sviluppo">Mai documenti veri dei clienti.</h2></div>
    <ul class="elenco-segni">
      <li>{ico("fingerprint")}<span>Proviamo i programmi solo su documenti inventati, con dati finti ma realistici: per esempio codici fiscali con il carattere di controllo corretto.</span></li>
      <li>{ico("list-checks")}<span>Per ogni documento di prova sappiamo in anticipo quali dati devono essere trovati, e misuriamo quanti ne troviamo davvero.</span></li>
      <li>{ico("lock-key")}<span>Il codice è conservato in un archivio privato, con accesso protetto da verifica in due passaggi.</span></li>
    </ul>
  </div>
</section>

<section class="sezione scura" aria-labelledby="t-sito">
  <div class="contenitore due-colonne">
    <div><div class="occhiello">Questo sito</div><h2 id="t-sito">Un sito che non ti osserva.</h2></div>
    <ul class="elenco-segni">
      <li>{ico("prohibit")}<span>Nessun cookie, nessuna statistica, nessuno strumento di tracciamento.</span></li>
      <li>{ico("cloud-slash")}<span>Nessuna risorsa caricata da altri siti: caratteri, icone e immagini sono ospitati insieme alle pagine.</span></li>
      <li>{ico("envelope-simple")}<span>Nessun modulo: per scriverci usi la tua posta. Dettagli nell'<a href="/privacy.html">informativa privacy</a>.</span></li>
    </ul>
  </div>
</section>

<section class="sezione" aria-labelledby="t-segnala">
  <div class="contenitore due-colonne">
    <div><div class="occhiello">Segnalazioni</div><h2 id="t-segnala">Hai trovato un problema di sicurezza?</h2></div>
    <div class="corpo">
      <p>Scrivici a <a href="mailto:{EMAIL}?subject=Segnalazione%20di%20sicurezza">{EMAIL}</a> con oggetto "Segnalazione di sicurezza". Descrivi il problema e come riprodurlo, senza allegare dati personali reali.</p>
      <p>Ti rispondiamo per iscritto e ti teniamo aggiornato fino alla soluzione. Le stesse indicazioni sono nel file <a href="/.well-known/security.txt">security.txt</a>.</p>
    </div>
  </div>
</section>'''
pagina("sicurezza.html", "Sicurezza — Taloryn Labs",
       "Come Taloryn Labs protegge i dati: programmi che lavorano sul tuo computer senza internet, verifica finale bloccante, sito senza cookie né tracciamento.",
       "/sicurezza.html", sic)

# ------------------------------------------------------------------ GUIDE
GUIDE = [
    ("coprire-non-e-cancellare.html", "Coprire non è cancellare: perché un rettangolo nero non basta",
     "Che cosa resta dentro un PDF o un file Word quando un dato viene solo coperto, e perché chi riceve il file può ancora leggerlo.", "5 minuti"),
    ("controllare-pdf-oscurato.html", "Come controllare se un documento oscurato è davvero pulito",
     "Quattro controlli che puoi fare in pochi minuti, con i programmi che hai già, prima di inviare un PDF o un file Word.", "6 minuti"),
    ("codici-di-controllo.html", "Codice fiscale, partita IVA e IBAN: il controllo che non sbaglia",
     "Come funzionano i caratteri di controllo e perché permettono di riconoscere questi dati con certezza.", "7 minuti"),
]
schede_guide = "".join(
    f'<a class="guida" href="/guide/{f}"><span class="meta">Lettura: {t}</span><h3>{h}</h3><p>{d}</p><span class="leggi">Leggi la guida{ico("arrow-right", "regular")}</span></a>'
    for f, h, d, t in GUIDE)
guide_idx = f'''<section class="testa-pagina" aria-labelledby="t-guide">
  <div class="contenitore">
    <div class="occhiello">Guide</div>
    <h1 id="t-guide">Guide pratiche sui dati nei documenti.</h1>
    <p class="introduzione" style="margin-top:24px">Spiegazioni brevi e concrete per chi lavora in uno studio. Valgono anche se non usi i nostri programmi.</p>
  </div>
</section>
<section class="sezione" aria-label="Elenco delle guide">
  <div class="contenitore"><div class="elenco-guide">{schede_guide}</div>
  <p class="nota" style="margin-top:28px">Le guide hanno scopo informativo e non sono una consulenza legale.</p></div>
</section>'''
pagina("guide/index.html", "Guide — Taloryn Labs",
       "Guide pratiche per studi professionali: come oscurare davvero i dati nei PDF e nei file Word e come controllare un documento prima di inviarlo.",
       "/guide/", guide_idx)


def articolo(file, titolo_breve, descr, durata, corpo):
    c = f'''<article class="articolo">
  <div class="contenitore">
    <div class="briciole"><a href="/guide/">Guide</a> / {titolo_breve}</div>
    <h1>{titolo_breve}</h1>
    <p class="nota" style="margin-top:14px">Lettura: {durata} · Aggiornata il {AGGIORNATO}</p>
    <p class="introduzione" style="margin-top:22px">{descr}</p>
    {corpo}
    <div class="riquadro-nota"><p>Questa guida ha scopo informativo e non è una consulenza legale. Per gli obblighi del tuo studio fai riferimento al tuo consulente o all'ordine professionale.</p></div>
    <p><a class="secondario" href="/guide/">{ico("arrow-left", "regular")}Tutte le guide</a></p>
  </div>
</article>'''
    pagina(f"guide/{file}", f"{titolo_breve} — Guide Taloryn Labs", descr, "/guide/", c)


g = {f: (h, d, t) for f, h, d, t in GUIDE}

articolo("coprire-non-e-cancellare.html", *g["coprire-non-e-cancellare.html"], corpo='''
<h2>Che cosa succede quando "copri" un dato</h2>
<p>Molti programmi permettono di disegnare un rettangolo nero sopra una parte di un PDF, o di evidenziare un testo in nero. A colpo d'occhio il dato sparisce. Ma nella maggior parte dei casi hai solo aggiunto qualcosa <strong>sopra</strong> la pagina: il testo originale è ancora lì, sotto.</p>
<p>Un PDF è fatto a strati. Il testo è uno strato, i disegni e le annotazioni sono altri strati. Un rettangolo nero è un disegno: copre il testo alla vista, ma non lo toglie. Chi riceve il file può selezionare la zona coperta, copiarla e incollarla in un qualsiasi editor di testo, e leggere tutto.</p>

<h2>Le parti del file che non vedi</h2>
<p>Anche quando il testo visibile è stato tolto davvero, un documento può contenere altre informazioni:</p>
<ul>
  <li><strong>Metadati</strong>: il nome dell'autore, il titolo originale, a volte il nome del cliente nel titolo del file.</li>
  <li><strong>Commenti e note</strong>, anche quelli già "risolti".</li>
  <li><strong>Allegati</strong> inseriti nel PDF.</li>
  <li><strong>Revisioni</strong> nei file Word: con le revisioni attive, le versioni precedenti del testo restano nel documento finché non vengono accettate o rifiutate.</li>
  <li><strong>Livelli e campi nascosti</strong>, come testo bianco su sfondo bianco o campi di moduli compilati.</li>
</ul>

<h2>Perché oggi è più importante</h2>
<p>Un documento oscurato male non viene più letto solo da una persona. Sempre più spesso viene caricato in uno strumento di intelligenza artificiale per un riassunto o una traduzione. Molti di questi strumenti leggono il testo contenuto nel file, non l'immagine della pagina: per loro un rettangolo nero disegnato sopra non conta, e il dato sotto resta leggibile.</p>

<h2>Come si oscura davvero</h2>
<p>Oscurare davvero significa <strong>togliere il dato dal file</strong> e poi controllare il risultato. In pratica:</p>
<ol>
  <li>usare uno strumento che rimuove il testo, e non solo lo copre;</li>
  <li>eliminare metadati, commenti, allegati e revisioni;</li>
  <li>rileggere il file finale per verificare che il dato non ci sia più.</li>
</ol>
<p>Se vuoi controllare un documento che hai già, trovi i passaggi nella guida <a href="/guide/controllare-pdf-oscurato.html">Come controllare se un documento oscurato è davvero pulito</a>.</p>
''')

articolo("controllare-pdf-oscurato.html", *g["controllare-pdf-oscurato.html"], corpo='''
<div class="riquadro-nota"><p><strong>Prima di iniziare</strong>: fai questi controlli su una <strong>copia</strong> del documento, non sull'originale.</p></div>

<h2>1. Copia e incolla il testo</h2>
<p>È il controllo più semplice ed è quello che rivela più problemi.</p>
<ol>
  <li>Apri il PDF con il programma che usi di solito, per esempio Adobe Acrobat Reader o il browser.</li>
  <li>Premi <span class="tasto">Ctrl</span> + <span class="tasto">A</span> per selezionare tutto il testo, poi <span class="tasto">Ctrl</span> + <span class="tasto">C</span> per copiarlo.</li>
  <li>Apri il Blocco note di Windows e premi <span class="tasto">Ctrl</span> + <span class="tasto">V</span>.</li>
  <li>Leggi il testo incollato: se compaiono i dati che pensavi di aver coperto, il documento non è pulito.</li>
</ol>

<h2>2. Cerca i dati</h2>
<p>Premi <span class="tasto">Ctrl</span> + <span class="tasto">F</span> e cerca un dato che dovrebbe essere stato tolto: un cognome, le prime lettere del codice fiscale, una parte dell'IBAN. Se la ricerca lo trova, il dato è ancora nel file, anche se sulla pagina vedi un rettangolo nero.</p>

<h2>3. Guarda le proprietà del documento</h2>
<p>In Adobe Acrobat Reader premi <span class="tasto">Ctrl</span> + <span class="tasto">D</span> per aprire le proprietà del documento. Controlla i campi Titolo, Autore, Oggetto e Parole chiave: a volte contengono il nome del cliente o il nome originale del file.</p>
<p>Controlla anche il pannello dei commenti e quello degli allegati, se il programma li mostra: possono contenere testo che non compare sulla pagina.</p>

<h2>4. Nei file Word: usa il controllo documento</h2>
<p>Word ha uno strumento che cerca commenti, revisioni, proprietà e testo nascosto. In Word per Windows:</p>
<ol>
  <li>apri la scheda <strong>File</strong> e scegli <strong>Informazioni</strong>;</li>
  <li>fai clic su <strong>Verifica documento</strong> e poi su <strong>Controlla documento</strong>;</li>
  <li>nella finestra <strong>Controllo documento</strong> lascia selezionate le voci e premi <strong>Controlla</strong>;</li>
  <li>accanto a ogni risultato puoi premere <strong>Rimuovi tutto</strong>.</li>
</ol>
<p>Attenzione: Microsoft avverte che il contenuto rimosso in questo modo potrebbe non essere recuperabile con il comando Annulla. Per questo è importante lavorare su una copia. Prima di inviare, controlla anche la scheda <strong>Revisione</strong>: se ci sono revisioni non accettate, il testo precedente è ancora nel file.</p>

<h2>Se un controllo fallisce</h2>
<p>Non basta coprire di nuovo. Il dato va tolto dal file, e il documento va controllato un'altra volta dall'inizio. È esattamente il lavoro che Riserbo fa in automatico: rimuove il dato, pulisce le parti nascoste e rilegge il file prima di salvarlo.</p>
''')

articolo("codici-di-controllo.html", *g["codici-di-controllo.html"], corpo='''
<h2>Perché un controllo matematico</h2>
<p>Riconoscere un dato "a occhio", per forma, porta a errori: una sequenza di 11 cifre può essere una partita IVA, ma anche un numero di pratica. Alcuni codici però hanno un <strong>carattere di controllo</strong>: l'ultimo carattere è calcolato dagli altri con una formula precisa. Se il calcolo non torna, quel codice non è valido, oppure contiene un errore di battitura.</p>
<p>Per un programma questo è prezioso: permette di dire con certezza "questo è un codice fiscale", invece di "sembra un codice fiscale".</p>

<h2>Il codice fiscale</h2>
<p>Il codice fiscale delle persone fisiche ha 16 caratteri: tre lettere per il cognome, tre per il nome, l'anno, il mese (con una lettera) e il giorno di nascita (al giorno si aggiunge 40 per le donne), il codice del comune o dello Stato estero di nascita e infine il <strong>carattere di controllo</strong>.</p>
<p>Il carattere di controllo si ottiene così: a ogni carattere dei primi 15 si assegna un valore, con una tabella per le posizioni dispari e una per quelle pari; si sommano i valori, si divide per 26 e il resto indica la lettera, da A a Z.</p>
<p>Esempio con dati inventati: <span class="codice">BNCLRA82M45G388D</span>. Laura Bianchi, nata il 5 agosto 1982 a Pavia: il giorno è 45 perché 5 + 40, la M sta per agosto, G388 è Pavia, e la D finale è il risultato del calcolo.</p>
<h3>Le omocodie</h3>
<p>Due persone diverse possono avere gli stessi primi 15 caratteri. In quel caso l'Agenzia delle Entrate sostituisce alcune cifre con lettere (0 diventa L, 1 diventa M, e così via fino a 9 che diventa V), partendo da destra. Un programma serio deve riconoscere anche questi codici, ricalcolando il carattere di controllo.</p>

<h2>La partita IVA</h2>
<p>La partita IVA ha 11 cifre: le prime 7 identificano il soggetto, le 3 successive l'ufficio provinciale, l'ultima è la <strong>cifra di controllo</strong>.</p>
<p>Il calcolo è quello di Luhn: le cifre in posizione dispari si sommano così come sono; quelle in posizione pari si raddoppiano e, se il risultato supera 9, si toglie 9; si sommano tutti i valori e la cifra di controllo è quella che porta il totale al multiplo di 10 successivo.</p>

<h2>L'IBAN</h2>
<p>L'IBAN italiano ha 27 caratteri: <span class="codice">IT</span>, due cifre di controllo, il CIN (una lettera di controllo nazionale), il codice ABI della banca (5 cifre), il CAB dello sportello (5 cifre) e il numero di conto (12 caratteri).</p>
<p>Il controllo internazionale funziona così: si spostano i primi 4 caratteri in fondo, si trasformano le lettere in numeri (A = 10, B = 11 e così via) e si divide il numero ottenuto per 97. Se il resto è 1, l'IBAN è formalmente corretto.</p>
<p>Esempio molto usato nei manuali: <span class="codice">IT60 X054 2811 1010 0000 0123 456</span>. Il calcolo dà resto 1.</p>

<h2>Che cosa non dice il controllo</h2>
<p>Un codice che supera il controllo è <strong>scritto correttamente</strong>, ma il calcolo non dice se esiste davvero o a chi appartiene. Per oscurare un documento non serve saperlo: basta sapere con certezza che quel dato è un codice fiscale, una partita IVA o un IBAN, e toglierlo.</p>
<p>È il principio su cui si basa Riserbo: dove esiste un controllo matematico lo usa, e quello che non può verificare con certezza lo segnala a te.</p>
''')

# ------------------------------------------------------------------ CONTATTI
contatti = f'''<section class="testa-pagina" aria-labelledby="t-contatti">
  <div class="contenitore">
    <div class="occhiello">Contatti</div>
    <h1 id="t-contatti">Scrivici. Rispondiamo per iscritto.</h1>
    <p class="introduzione" style="margin-top:24px">Non abbiamo un centralino: tutto passa per email, così ogni domanda e ogni risposta restano agli atti, per te e per noi.</p>
  </div>
</section>
<section class="sezione" aria-label="Indirizzi">
  <div class="contenitore">
    <div class="contatti">
      <div class="scheda"><div class="icona">{ico("envelope-simple")}</div><h3>Informazioni</h3><p>Domande sullo studio e sui prodotti.</p><p style="margin-top:12px"><a href="mailto:info@talorynlabs.it">info@talorynlabs.it</a></p></div>
      <div class="scheda"><div class="icona">{ico("chat-text")}</div><h3>Assistenza</h3><p>Per chi usa i nostri programmi.</p><p style="margin-top:12px"><a href="mailto:support@talorynlabs.it">support@talorynlabs.it</a></p></div>
      <div class="scheda"><div class="icona">{ico("shield-check")}</div><h3>Privacy</h3><p>Richieste sui tuoi dati personali.</p><p style="margin-top:12px"><a href="mailto:privacy@talorynlabs.it">privacy@talorynlabs.it</a></p></div>
    </div>
  </div>
</section>
<section class="sezione scura" id="lista-attesa" aria-labelledby="t-attesa">
  <div class="contenitore due-colonne">
    <div><div class="occhiello">Lista d'attesa</div><h2 id="t-attesa">Entra nella lista d'attesa di Riserbo.</h2></div>
    <div class="corpo">
      <p>Scrivici da un indirizzo del tuo studio. Ti avvisiamo <strong>una sola volta</strong>, quando il programma sarà disponibile. Se vuoi, indicaci che tipo di studio sei: ci aiuta a preparare i documenti di prova giusti.</p>
      <div class="azioni" style="margin-top:20px"><a class="pulsante" href="{ATTESA}">{ico("envelope-simple", "regular")}Scrivi a info@talorynlabs.it</a></div>
      <p class="nota" style="margin-top:20px">Usiamo il tuo indirizzo solo per questo avviso. Nessun modulo, nessun servizio esterno. Dettagli nell'<a href="/privacy.html">informativa privacy</a>.</p>
    </div>
  </div>
</section>'''
pagina("contatti.html", "Contatti — Taloryn Labs",
       "Scrivi a Taloryn Labs: informazioni, assistenza, privacy e lista d'attesa di Riserbo. Rispondiamo per iscritto.",
       "/contatti.html", contatti, fascia=False)

# ------------------------------------------------------------------ PRIVACY
privacy = f'''<section class="testa-pagina" aria-labelledby="t-privacy">
  <div class="contenitore">
    <div class="occhiello">Note legali</div>
    <h1 id="t-privacy">Informativa privacy</h1>
    <p class="nota" style="margin-top:18px">Ultimo aggiornamento: {AGGIORNATO}.</p>
  </div>
</section>
<section class="testo-legale">
  <div class="contenitore">
    <h2>Chi tratta i dati</h2>
    <p>Titolare del trattamento: Taloryn Labs. Contatto: <a href="mailto:privacy@talorynlabs.it">privacy@talorynlabs.it</a> (oppure <a href="mailto:{EMAIL}">{EMAIL}</a>).</p>

    <h2>Visita del sito</h2>
    <p>Il sito non usa cookie, non usa strumenti di statistica o di tracciamento e non carica risorse da altri siti: caratteri, icone e immagini sono ospitati insieme alle pagine.</p>
    <p>Il sito è ospitato da GitHub Pages (GitHub, Inc.). Come ogni servizio di hosting, GitHub registra l'indirizzo IP di chi visita le pagine per garantire la sicurezza e il funzionamento del servizio. Noi non abbiamo accesso a questi dati. Per i dettagli si veda l'informativa privacy di GitHub.</p>

    <h2>Email e lista d'attesa</h2>
    <p>Se ci scrivi, per una domanda o per entrare nella lista d'attesa, trattiamo il tuo indirizzo email e quello che scegli di scriverci nel messaggio.</p>
    <ul>
      <li><strong>Perché:</strong> per risponderti e, se ti iscrivi alla lista d'attesa, per avvisarti una sola volta quando Riserbo sarà disponibile.</li>
      <li><strong>Base giuridica:</strong> la tua richiesta (art. 6, par. 1, lett. b del Regolamento UE 2016/679).</li>
      <li><strong>Dove:</strong> nella nostra casella di posta presso il fornitore del dominio talorynlabs.it. Non usiamo servizi di newsletter né moduli di terzi.</li>
      <li><strong>Per quanto:</strong> per la lista d'attesa fino all'invio dell'avviso, e comunque non oltre 24 mesi; poi il messaggio viene cancellato.</li>
      <li><strong>A chi:</strong> a nessuno. Non vendiamo né cediamo dati.</li>
    </ul>

    <h2>I tuoi diritti</h2>
    <p>Puoi chiedere in qualsiasi momento di vedere, correggere o cancellare i tuoi dati, oppure di essere tolto dalla lista, scrivendo a <a href="mailto:privacy@talorynlabs.it">privacy@talorynlabs.it</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali (garanteprivacy.it).</p>

    <h2>Il programma Riserbo</h2>
    <p>Il programma elabora i documenti solo sul tuo computer e non si collega a internet: i documenti che apri non arrivano mai a noi.</p>
  </div>
</section>'''
pagina("privacy.html", "Informativa privacy — Taloryn Labs",
       "Come Taloryn Labs tratta i dati di chi visita il sito e di chi scrive o si iscrive alla lista d'attesa.",
       "", privacy, fascia=False)

# ------------------------------------------------------------------ TERMINI
termini = f'''<section class="testa-pagina" aria-labelledby="t-termini">
  <div class="contenitore">
    <div class="occhiello">Note legali</div>
    <h1 id="t-termini">Condizioni d'uso del sito</h1>
    <p class="nota" style="margin-top:18px">Ultimo aggiornamento: {AGGIORNATO}.</p>
  </div>
</section>
<section class="testo-legale">
  <div class="contenitore">
    <h2>Chi gestisce il sito</h2>
    <p>Il sito talorynlabs.it è gestito da Taloryn Labs. Contatto: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

    <h2>A cosa serve il sito</h2>
    <p>Il sito presenta lo studio e i suoi prodotti. Al momento non vende nulla: Riserbo è in sviluppo e le descrizioni indicano come sarà il prodotto secondo la specifica approvata. Le funzioni e i tempi possono cambiare prima dell'uscita; le eventuali modifiche saranno riportate su queste pagine.</p>

    <h2>Licenza dei programmi</h2>
    <p>Le condizioni di licenza di Riserbo, il prezzo e le condizioni della prova gratuita saranno pubblicati su questo sito prima dell'uscita, e andranno accettati al momento dell'acquisto. Queste condizioni d'uso riguardano solo il sito.</p>

    <h2>Contenuti e guide</h2>
    <p>Le guide e gli altri testi hanno scopo informativo. Li scriviamo con cura e li aggiorniamo, ma non sono una consulenza legale, fiscale o tecnica sul tuo caso specifico.</p>

    <h2>Nome, simbolo e testi</h2>
    <p>Il nome Taloryn Labs, il simbolo della T d'oro, i testi e le immagini di questo sito appartengono a Taloryn Labs. Puoi citarli e condividere i collegamenti alle pagine; per altri usi scrivici.</p>

    <h2>Riconoscimenti</h2>
    <p>Il sito usa il carattere Montserrat (licenza SIL Open Font License 1.1) e le icone Phosphor (licenza MIT). I testi delle licenze sono pubblicati insieme ai file: <a href="/font/LICENZA-montserrat.txt">licenza Montserrat</a>, <a href="/font/LICENZA-phosphor-icons.txt">licenza Phosphor</a>.</p>

    <h2>Modifiche e legge applicabile</h2>
    <p>Possiamo aggiornare queste condizioni; la data in alto indica l'ultima versione. Si applica la legge italiana.</p>
  </div>
</section>'''
pagina("termini.html", "Condizioni d'uso — Taloryn Labs",
       "Condizioni d'uso del sito talorynlabs.it: chi lo gestisce, a cosa serve, contenuti, licenze e riconoscimenti.",
       "", termini, fascia=False)

# ------------------------------------------------------------------ 404
nf = f'''<section class="testa-pagina" aria-labelledby="t-404">
  <div class="contenitore">
    <div class="occhiello">Errore 404</div>
    <h1 id="t-404">Questa pagina non esiste.</h1>
    <p class="introduzione" style="margin-top:24px">Forse il collegamento è sbagliato, o la pagina è stata spostata.</p>
    <div class="azioni"><a class="pulsante" href="/">Torna alla pagina principale{ico("arrow-right", "regular")}</a><a class="secondario" href="/guide/">Vai alle guide</a></div>
  </div>
</section>'''
pagina("404.html", "Pagina non trovata — Taloryn Labs", "La pagina cercata non esiste.", "", nf, fascia=False)

# ------------------------------------------------------------------ vecchio indirizzo
# il prodotto si chiamava "PDF Suite Desktop" (nome di lavoro, cambiato il 29 ottobre 2026): chi ha il
# vecchio collegamento arriva alla pagina nuova (rimando HTML, nessuno script; non è nella mappa del sito)
(OUT / "pdf-suite.html").write_text(f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Riserbo — Taloryn Labs</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{DOMINIO}/riserbo.html">
<meta http-equiv="refresh" content="0; url=/riserbo.html">
</head>
<body><p>La pagina si è spostata: <a href="/riserbo.html">Riserbo</a>.</p></body>
</html>
''', encoding="utf-8")

# ------------------------------------------------------------------ file di servizio
pagine = ["", "riserbo.html", "sicurezza.html", "guide/", *[f"guide/{f}" for f, *_ in GUIDE],
          "contatti.html", "privacy.html", "termini.html"]
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{DOMINIO}/{p}</loc><lastmod>2026-10-22</lastmod></url>\n" for p in pagine)
    + "</urlset>\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
(OUT / ".well-known" / "security.txt").write_text(
    f"Contact: mailto:{EMAIL}\nExpires: 2027-10-22T00:00:00.000Z\nPreferred-Languages: it, en\n"
    f"Canonical: {DOMINIO}/.well-known/security.txt\nPolicy: {DOMINIO}/sicurezza.html\n", encoding="utf-8")
print("ok", len(pagine) + 1, "pagine")
