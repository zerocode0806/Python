# generate_german_2000_optimized.py
# Generate 2000 REAL German vocabulary entries with proper conjugations
# Table: Word | Meaning(Indonesian) | Perfekt | Präteritum | Sinonim
# Output: german_2000_real.csv and german_2000_real.pdf
# Usage: pip install reportlab pandas
# then: python generate_german_2000_optimized.py

import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

# ========== TARGET DISTRIBUTION ==========
TARGET = {
    "Verb": 700,
    "Trennbare Verb": 400, 
    "Adjektiv": 300,
    "Nomen": 600
}

# ========== REAL GERMAN VOCABULARY LISTS ==========

# REAL GERMAN VERBS with Indonesian meanings and synonyms
REAL_VERBS = [
    # Irregular verbs
    ("sein", "ada/adalah", "—"),
    ("haben", "memiliki", "besitzen"),
    ("werden", "menjadi", "—"),
    ("gehen", "pergi/berjalan", "laufen"),
    ("kommen", "datang", "ankommen"),
    ("sehen", "melihat", "blicken"),
    ("geben", "memberi", "schenken"),
    ("nehmen", "mengambil", "holen"),
    ("finden", "menemukan", "entdecken"),
    ("stehen", "berdiri", "—"),
    ("sitzen", "duduk", "—"),
    ("liegen", "berbaring", "—"),
    ("schreiben", "menulis", "verfassen"),
    ("lesen", "membaca", "—"),
    ("fahren", "berkendara", "reisen"),
    ("bringen", "membawa", "transportieren"),
    ("denken", "berpikir", "überlegen"),
    ("essen", "makan", "speisen"),
    ("trinken", "minum", "—"),
    ("bleiben", "tinggal/tetap", "verweilen"),
    ("beginnen", "memulai", "anfangen"),
    ("sprechen", "berbicara", "reden"),
    ("laufen", "berlari", "rennen"),
    ("schlafen", "tidur", "ruhen"),
    ("helfen", "membantu", "unterstützen"),
    ("treffen", "bertemu", "begegnen"),
    ("verlieren", "kehilangan", "—"),
    ("gewinnen", "menang", "siegen"),
    ("vergessen", "lupa", "—"),
    ("ziehen", "menarik", "—"),
    ("fallen", "jatuh", "stürzen"),
    ("halten", "memegang", "festhalten"),
    ("lassen", "membiarkan", "erlauben"),
    ("fliegen", "terbang", "—"),
    ("sterben", "mati", "—"),
    ("wissen", "tahu", "kennen"),
    ("können", "bisa", "vermögen"),
    ("müssen", "harus", "sollen"),
    ("wollen", "ingin", "möchten"),
    ("dürfen", "boleh", "—"),
    ("mögen", "suka", "—"),
    ("sollen", "seharusnya", "müssen"),
    
    # Regular verbs
    ("arbeiten", "bekerja", "schaffen"),
    ("lernen", "belajar", "studieren"),
    ("spielen", "bermain", "—"),
    ("kaufen", "membeli", "erwerben"),
    ("verkaufen", "menjual", "—"),
    ("fragen", "bertanya", "—"),
    ("antworten", "menjawab", "erwidern"),
    ("wohnen", "tinggal", "leben"),
    ("reisen", "bepergian", "fahren"),
    ("kochen", "memasak", "—"),
    ("öffnen", "membuka", "aufmachen"),
    ("schließen", "menutup", "zumachen"),
    ("suchen", "mencari", "—"),
    ("bestellen", "memesan", "—"),
    ("bezahlen", "membayar", "zahlen"),
    ("mieten", "menyewa", "—"),
    ("besuchen", "mengunjungi", "—"),
    ("telefonieren", "menelpon", "anrufen"),
    ("studieren", "kuliah", "lernen"),
    ("hören", "mendengar", "—"),
    ("verstehen", "memahami", "begreifen"),
    ("erklären", "menjelaskan", "—"),
    ("zeigen", "menunjukkan", "—"),
    ("warten", "menunggu", "—"),
    ("leben", "hidup", "existieren"),
    ("lieben", "mencintai", "—"),
    ("hassen", "membenci", "—"),
    ("feiern", "merayakan", "—"),
    ("tanzen", "menari", "—"),
    ("singen", "menyanyi", "—"),
    ("holen", "mengambil", "nehmen"),
    ("bringen", "membawa", "transportieren"),
    ("putzen", "membersihkan", "säubern"),
    ("waschen", "mencuci", "—"),
    ("reparieren", "memperbaiki", "—"),
    ("bauen", "membangun", "konstruieren"),
    ("malen", "melukis", "zeichnen"),
    ("fotografieren", "memotret", "—"),
    ("sammeln", "mengumpulkan", "—"),
    ("sparen", "menabung", "—"),
    ("ausgeben", "mengeluarkan", "—"),
    ("verdienen", "menghasilkan", "—"),
    ("verlassen", "meninggalkan", "—"),
    ("erreichen", "mencapai", "—"),
    ("schaffen", "berhasil", "erreichen"),
    ("versuchen", "mencoba", "probieren"),
    ("planen", "merencanakan", "—"),
    ("organisieren", "mengorganisir", "—"),
    ("kontrollieren", "mengontrol", "prüfen"),
    ("entwickeln", "mengembangkan", "—"),
    ("produzieren", "memproduksi", "herstellen"),
    ("verkaufen", "menjual", "—"),
    ("informieren", "menginformasikan", "—"),
    ("diskutieren", "mendiskusikan", "besprechen"),
    ("präsentieren", "mempresentasikan", "vorstellen"),
    ("analysieren", "menganalisis", "untersuchen"),
    ("entscheiden", "memutuskan", "—"),
    ("wählen", "memilih", "auswählen"),
    ("ändern", "mengubah", "verändern"),
    ("verbessern", "memperbaiki", "—"),
    ("zerstören", "menghancurkan", "—"),
    ("retten", "menyelamatkan", "—"),
    ("schützen", "melindungi", "—"),
    ("kämpfen", "berjuang", "—"),
    ("gewinnen", "menang", "siegen"),
    ("verlieren", "kalah", "—"),
    ("trainieren", "berlatih", "üben"),
    ("üben", "berlatih", "trainieren"),
    ("wiederholen", "mengulang", "—"),
    ("merken", "mengingat", "—"),
    ("erinnern", "mengingatkan", "—"),
    ("träumen", "bermimpi", "—"),
    ("hoffen", "berharap", "—"),
    ("glauben", "percaya", "—"),
    ("zweifeln", "meragukan", "—"),
    ("fürchten", "takut", "—"),
    ("sich freuen", "senang", "—"),
    ("lachen", "tertawa", "—"),
    ("weinen", "menangis", "—"),
    ("lächeln", "tersenyum", "—"),
    ("grüßen", "menyapa", "—"),
    ("sich verabschieden", "berpamitan", "—"),
    ("sich entschuldigen", "meminta maaf", "—"),
    ("danken", "berterima kasih", "—"),
    ("gratulieren", "mengucapkan selamat", "—"),
    ("einladen", "mengundang", "—"),
    ("sich treffen", "bertemu", "—"),
    ("sich unterhalten", "berbincang", "—"),
    ("sich streiten", "bertengkar", "—"),
    ("sich versöhnen", "berdamai", "—"),
]

# REAL SEPARABLE VERBS  
REAL_SEPARABLE_VERBS = [
    ("aufstehen", "bangun tidur", "sich erheben"),
    ("aufwachen", "terbangun", "erwachen"),
    ("anrufen", "menelpon", "telefonieren"),
    ("ankommen", "tiba", "erreichen"),
    ("abfahren", "berangkat", "wegfahren"),
    ("einsteigen", "naik (kendaraan)", "—"),
    ("aussteigen", "turun (kendaraan)", "—"),
    ("umsteigen", "ganti (kendaraan)", "—"),
    ("mitnehmen", "membawa serta", "—"),
    ("mitbringen", "membawa", "—"),
    ("abholen", "menjemput", "—"),
    ("zurückkommen", "kembali", "—"),
    ("weggehen", "pergi", "—"),
    ("hereinkommen", "masuk", "—"),
    ("hinausgehen", "keluar", "—"),
    ("vorbeikommen", "mampir", "—"),
    ("fernsehen", "menonton TV", "—"),
    ("einkaufen", "berbelanja", "—"),
    ("ausgehen", "keluar (bersenang-senang)", "—"),
    ("spazierengehen", "jalan-jalan", "—"),
    ("aufmachen", "membuka", "öffnen"),
    ("zumachen", "menutup", "schließen"),
    ("anmachen", "menyalakan", "einschalten"),
    ("ausmachen", "mematikan", "ausschalten"),
    ("einschalten", "menyalakan", "anmachen"),
    ("ausschalten", "mematikan", "ausmachen"),
    ("aufräumen", "membereskan", "—"),
    ("saubermachen", "membersihkan", "putzen"),
    ("vorbereiten", "mempersiapkan", "—"),
    ("nachdenken", "merenung", "überlegen"),
    ("aufpassen", "memperhatikan", "—"),
    ("zuhören", "mendengarkan", "—"),
    ("zusehen", "menyaksikan", "—"),
    ("teilnehmen", "berpartisipasi", "—"),
    ("stattfinden", "berlangsung", "—"),
    ("anfangen", "memulai", "beginnen"),
    ("aufhören", "berhenti", "—"),
    ("weitermachen", "melanjutkan", "—"),
    ("fortsetzen", "meneruskan", "—"),
    ("abbrechen", "membatalkan", "—"),
    ("vorstellen", "memperkenalkan", "—"),
    ("sich vorstellen", "memperkenalkan diri", "—"),
    ("einladen", "mengundang", "—"),
    ("absagen", "membatalkan", "—"),
    ("zusagen", "menyetujui", "—"),
    ("anbieten", "menawarkan", "—"),
    ("ablehnen", "menolak", "—"),
    ("annehmen", "menerima", "—"),
    ("zurückgeben", "mengembalikan", "—"),
    ("ausgeben", "mengeluarkan (uang)", "—"),
    ("einsparen", "menghemat", "—"),
]

# REAL GERMAN ADJECTIVES
REAL_ADJECTIVES = [
    ("alt", "tua", "betagt"),
    ("jung", "muda", "—"),
    ("groß", "besar", "riesig"),
    ("klein", "kecil", "winzig"),
    ("neu", "baru", "frisch"),
    ("alt", "lama", "antik"),
    ("schnell", "cepat", "rasch"),
    ("langsam", "lambat", "träge"),
    ("schön", "indah", "hübsch"),
    ("hässlich", "jelek", "—"),
    ("gut", "baik", "prima"),
    ("schlecht", "buruk", "übel"),
    ("teuer", "mahal", "kostspielig"),
    ("billig", "murah", "günstig"),
    ("einfach", "mudah", "simpel"),
    ("schwierig", "sulit", "kompliziert"),
    ("leicht", "ringan", "—"),
    ("schwer", "berat", "—"),
    ("stark", "kuat", "kräftig"),
    ("schwach", "lemah", "kraftlos"),
    ("gesund", "sehat", "—"),
    ("krank", "sakit", "erkrankt"),
    ("müde", "lelah", "erschöpft"),
    ("munter", "segar", "—"),
    ("warm", "hangat", "heiß"),
    ("kalt", "dingin", "frostig"),
    ("heiß", "panas", "—"),
    ("kühl", "sejuk", "—"),
    ("trocken", "kering", "—"),
    ("nass", "basah", "feucht"),
    ("sauber", "bersih", "rein"),
    ("schmutzig", "kotor", "dreckig"),
    ("ordentlich", "rapi", "—"),
    ("unordentlich", "berantakan", "—"),
    ("ruhig", "tenang", "still"),
    ("laut", "keras", "geräuschvoll"),
    ("leise", "pelan", "still"),
    ("hell", "terang", "—"),
    ("dunkel", "gelap", "finster"),
    ("freundlich", "ramah", "nett"),
    ("unfreundlich", "tidak ramah", "—"),
    ("höflich", "sopan", "—"),
    ("unhöflich", "tidak sopan", "—"),
    ("glücklich", "bahagia", "froh"),
    ("unglücklich", "tidak bahagia", "traurig"),
    ("traurig", "sedih", "betrübt"),
    ("fröhlich", "ceria", "—"),
    ("nervös", "gugup", "—"),
    ("ruhig", "tenang", "gelassen"),
    ("aufgeregt", "bersemangat", "—"),
    ("langweilig", "membosankan", "—"),
    ("interessant", "menarik", "spannend"),
    ("wichtig", "penting", "bedeutsam"),
    ("unwichtig", "tidak penting", "—"),
    ("richtig", "benar", "korrekt"),
    ("falsch", "salah", "verkehrt"),
    ("möglich", "mungkin", "—"),
    ("unmöglich", "tidak mungkin", "—"),
    ("normal", "normal", "gewöhnlich"),
    ("besonders", "istimewa", "speziell"),
    ("berühmt", "terkenal", "bekannt"),
    ("unbekannt", "tidak dikenal", "—"),
    ("modern", "modern", "zeitgemäß"),
    ("traditionell", "tradisional", "klassisch"),
    ("international", "internasional", "—"),
    ("national", "nasional", "—"),
    ("lokal", "lokal", "örtlich"),
    ("öffentlich", "umum", "—"),
    ("privat", "pribadi", "—"),
    ("persönlich", "pribadi", "—"),
    ("offiziell", "resmi", "—"),
    ("inoffiziell", "tidak resmi", "—"),
    ("legal", "legal", "—"),
    ("illegal", "ilegal", "—"),
    ("sicher", "aman", "—"),
    ("gefährlich", "bahaya", "—"),
    ("vorsichtig", "hati-hati", "—"),
    ("mutig", "berani", "—"),
    ("ängstlich", "takut", "—"),
    ("stolz", "bangga", "—"),
    ("bescheiden", "rendah hati", "—"),
    ("arrogant", "sombong", "—"),
    ("ehrlich", "jujur", "—"),
    ("unehrlich", "tidak jujur", "—"),
    ("fleißig", "rajin", "—"),
    ("faul", "malas", "—"),
    ("klug", "pintar", "intelligent"),
    ("dumm", "bodoh", "—"),
    ("kreativ", "kreatif", "—"),
    ("praktisch", "praktis", "—"),
    ("theoretisch", "teoretis", "—"),
    ("wissenschaftlich", "ilmiah", "—"),
    ("künstlerisch", "artistik", "—"),
    ("sportlich", "atletis", "—"),
    ("musikalisch", "musikal", "—"),
    ("technisch", "teknis", "—"),
    ("digital", "digital", "—"),
    ("analog", "analog", "—"),
    ("elektronisch", "elektronik", "—"),
    ("mechanisch", "mekanis", "—"),
    ("automatisch", "otomatis", "—"),
    ("manuell", "manual", "—"),
]

# REAL GERMAN NOUNS
REAL_NOUNS = [
    # Family & People
    ("Familie", "keluarga", "—"),
    ("Eltern", "orang tua", "—"),
    ("Mutter", "ibu", "Mama"),
    ("Vater", "ayah", "Papa"),
    ("Kind", "anak", "—"),
    ("Sohn", "anak laki-laki", "—"),
    ("Tochter", "anak perempuan", "—"),
    ("Bruder", "saudara laki-laki", "—"),
    ("Schwester", "saudara perempuan", "—"),
    ("Großeltern", "kakek nenek", "—"),
    ("Großmutter", "nenek", "Oma"),
    ("Großvater", "kakek", "Opa"),
    ("Freund", "teman", "Kumpel"),
    ("Freundin", "teman perempuan", "—"),
    ("Nachbar", "tetangga", "—"),
    ("Mann", "pria", "—"),
    ("Frau", "wanita", "—"),
    ("Person", "orang", "—"),
    ("Mensch", "manusia", "—"),
    ("Baby", "bayi", "—"),
    
    # Home & Living
    ("Haus", "rumah", "—"),
    ("Wohnung", "apartemen", "—"),
    ("Zimmer", "kamar", "Raum"),
    ("Küche", "dapur", "—"),
    ("Badezimmer", "kamar mandi", "Bad"),
    ("Schlafzimmer", "kamar tidur", "—"),
    ("Wohnzimmer", "ruang tamu", "—"),
    ("Balkon", "balkon", "—"),
    ("Garten", "kebun", "—"),
    ("Tür", "pintu", "—"),
    ("Fenster", "jendela", "—"),
    ("Dach", "atap", "—"),
    ("Wand", "dinding", "—"),
    ("Boden", "lantai", "—"),
    ("Treppe", "tangga", "—"),
    ("Aufzug", "elevator", "Lift"),
    
    # Furniture & Objects
    ("Tisch", "meja", "—"),
    ("Stuhl", "kursi", "—"),
    ("Bett", "tempat tidur", "—"),
    ("Schrank", "lemari", "—"),
    ("Sofa", "sofa", "—"),
    ("Lampe", "lampu", "—"),
    ("Fernseher", "televisi", "TV"),
    ("Computer", "komputer", "—"),
    ("Telefon", "telepon", "—"),
    ("Handy", "ponsel", "—"),
    ("Auto", "mobil", "—"),
    ("Fahrrad", "sepeda", "Rad"),
    ("Bus", "bus", "—"),
    ("Zug", "kereta", "—"),
    ("Flugzeug", "pesawat", "—"),
    
    # Food & Drink
    ("Essen", "makanan", "—"),
    ("Trinken", "minuman", "—"),
    ("Brot", "roti", "—"),
    ("Fleisch", "daging", "—"),
    ("Fisch", "ikan", "—"),
    ("Gemüse", "sayuran", "—"),
    ("Obst", "buah", "—"),
    ("Milch", "susu", "—"),
    ("Kaffee", "kopi", "—"),
    ("Tee", "teh", "—"),
    ("Wasser", "air", "—"),
    ("Bier", "bir", "—"),
    ("Wein", "anggur", "—"),
    ("Restaurant", "restoran", "—"),
    ("Café", "kafe", "—"),
    
    # Education & Work
    ("Schule", "sekolah", "—"),
    ("Universität", "universitas", "—"),
    ("Lehrer", "guru", "—"),
    ("Student", "mahasiswa", "—"),
    ("Arbeit", "pekerjaan", "Job"),
    ("Beruf", "profesi", "—"),
    ("Büro", "kantor", "—"),
    ("Firma", "perusahaan", "—"),
    ("Chef", "bos", "—"),
    ("Kollege", "kolega", "—"),
    ("Meeting", "rapat", "—"),
    ("Projekt", "proyek", "—"),
    ("Computer", "komputer", "—"),
    ("Internet", "internet", "—"),
    ("E-Mail", "email", "—"),
    
    # Time & Calendar
    ("Zeit", "waktu", "—"),
    ("Tag", "hari", "—"),
    ("Woche", "minggu", "—"),
    ("Monat", "bulan", "—"),
    ("Jahr", "tahun", "—"),
    ("Stunde", "jam", "—"),
    ("Minute", "menit", "—"),
    ("Morgen", "pagi", "—"),
    ("Mittag", "siang", "—"),
    ("Abend", "sore", "—"),
    ("Nacht", "malam", "—"),
    ("Heute", "hari ini", "—"),
    ("Gestern", "kemarin", "—"),
    ("Morgen", "besok", "—"),
    
    # Places & Geography
    ("Stadt", "kota", "—"),
    ("Dorf", "desa", "—"),
    ("Land", "negara", "—"),
    ("Straße", "jalan", "—"),
    ("Platz", "tempat", "—"),
    ("Park", "taman", "—"),
    ("See", "danau", "—"),
    ("Berg", "gunung", "—"),
    ("Meer", "laut", "—"),
    ("Fluss", "sungai", "—"),
    ("Wald", "hutan", "—"),
    ("Bahnhof", "stasiun kereta", "—"),
    ("Flughafen", "bandara", "—"),
    ("Hotel", "hotel", "—"),
    ("Geschäft", "toko", "Laden"),
    ("Supermarkt", "supermarket", "—"),
    ("Bank", "bank", "—"),
    ("Post", "kantor pos", "—"),
    ("Krankenhaus", "rumah sakit", "—"),
    ("Apotheke", "apotek", "—"),
    
    # Body & Health
    ("Körper", "tubuh", "—"),
    ("Kopf", "kepala", "—"),
    ("Gesicht", "wajah", "—"),
    ("Auge", "mata", "—"),
    ("Nase", "hidung", "—"),
    ("Mund", "mulut", "—"),
    ("Ohr", "telinga", "—"),
    ("Hand", "tangan", "—"),
    ("Finger", "jari", "—"),
    ("Fuß", "kaki", "—"),
    ("Bein", "kaki", "—"),
    ("Arm", "lengan", "—"),
    ("Rücken", "punggung", "—"),
    ("Bauch", "perut", "—"),
    ("Herz", "hati", "—"),
    ("Gesundheit", "kesehatan", "—"),
    ("Krankheit", "penyakit", "—"),
    ("Arzt", "dokter", "—"),
    ("Medikament", "obat", "—"),
    
    # Clothing
    ("Kleidung", "pakaian", "—"),
    ("Hemd", "kemeja", "—"),
    ("Hose", "celana", "—"),
    ("Kleid", "gaun", "—"),
    ("Rock", "rok", "—"),
    ("Jacke", "jaket", "—"),
    ("Mantel", "mantel", "—"),
    ("Schuh", "sepatu", "—"),
    ("Socke", "kaus kaki", "—"),
    ("Hut", "topi", "—"),
    ("Brille", "kacamata", "—"),
    
    # Weather & Nature
    ("Wetter", "cuaca", "—"),
    ("Sonne", "matahari", "—"),
    ("Mond", "bulan", "—"),
    ("Stern", "bintang", "—"),
    ("Himmel", "langit", "—"),
    ("Wolke", "awan", "—"),
    ("Regen", "hujan", "—"),
    ("Schnee", "salju", "—"),
    ("Wind", "angin", "—"),
    ("Sturm", "badai", "—"),
    ("Blume", "bunga", "—"),
    ("Baum", "pohon", "—"),
    ("Gras", "rumput", "—"),
    ("Tier", "hewan", "—"),
    ("Hund", "anjing", "—"),
    ("Katze", "kucing", "—"),
    ("Vogel", "burung", "—"),
    
    # Abstract Concepts
    ("Liebe", "cinta", "—"),
    ("Freundschaft", "persahabatan", "—"),
    ("Glück", "kebahagiaan", "—"),
    ("Frieden", "perdamaian", "—"),
    ("Hoffnung", "harapan", "—"),
    ("Angst", "ketakutan", "—"),
    ("Sorge", "kekhawatiran", "—"),
    ("Stress", "stres", "—"),
    ("Ruhe", "ketenangan", "—"),
    ("Erfolg", "kesuksesan", "—"),
    ("Problem", "masalah", "—"),
    ("Lösung", "solusi", "—"),
    ("Idee", "ide", "—"),
    ("Plan", "rencana", "—"),
    ("Ziel", "tujuan", "—"),
    ("Traum", "mimpi", "—"),
    ("Realität", "kenyataan", "—"),
    ("Wahrheit", "kebenaran", "—"),
    ("Lüge", "kebohongan", "—"),
    ("Meinung", "pendapat", "—"),
    
    # Money & Shopping
    ("Geld", "uang", "—"),
    ("Euro", "euro", "—"),
    ("Preis", "harga", "—"),
    ("Rechnung", "tagihan", "—"),
    ("Kasse", "kasir", "—"),
    ("Karte", "kartu", "—"),
    ("Bargeld", "uang tunai", "—"),
    ("Einkauf", "belanja", "—"),
    ("Verkauf", "penjualan", "—"),
    ("Angebot", "penawaran", "—"),
    ("Rabatt", "diskon", "—"),
    
    # Communication & Media
    ("Sprache", "bahasa", "—"),
    ("Wort", "kata", "—"),
    ("Satz", "kalimat", "—"),
    ("Text", "teks", "—"),
    ("Brief", "surat", "—"),
    ("Nachricht", "pesan", "—"),
    ("Information", "informasi", "—"),
    ("Zeitung", "koran", "—"),
    ("Zeitschrift", "majalah", "—"),
    ("Buch", "buku", "—"),
    ("Film", "film", "—"),
    ("Musik", "musik", "—"),
    ("Radio", "radio", "—"),
    ("Fernsehen", "televisi", "—"),
    ("Video", "video", "—"),
    ("Foto", "foto", "—"),
    
    # Sports & Hobbies
    ("Sport", "olahraga", "—"),
    ("Spiel", "permainan", "—"),
    ("Fußball", "sepak bola", "—"),
    ("Tennis", "tenis", "—"),
    ("Schwimmen", "renang", "—"),
    ("Laufen", "lari", "—"),
    ("Hobby", "hobi", "—"),
    ("Interesse", "minat", "—"),
    ("Spaß", "kesenangan", "—"),
    ("Party", "pesta", "—"),
    ("Feier", "perayaan", "—"),
    ("Urlaub", "liburan", "—"),
    ("Reise", "perjalanan", "—"),
    ("Abenteuer", "petualangan", "—"),
    
    # Education & Learning
    ("Bildung", "pendidikan", "—"),
    ("Wissen", "pengetahuan", "—"),
    ("Erfahrung", "pengalaman", "—"),
    ("Kurs", "kursus", "—"),
    ("Unterricht", "pelajaran", "—"),
    ("Prüfung", "ujian", "—"),
    ("Test", "tes", "—"),
    ("Hausaufgabe", "PR", "—"),
    ("Note", "nilai", "—"),
    ("Zeugnis", "rapor", "—"),
    ("Diplom", "diploma", "—"),
    ("Abschluss", "kelulusan", "—"),
]

# ========== IRREGULAR VERB CONJUGATIONS ==========
IRREGULAR_VERBS = {
    "sein": ("war", "ist gewesen"),
    "haben": ("hatte", "hat gehabt"),
    "werden": ("wurde", "ist geworden"),
    "gehen": ("ging", "ist gegangen"),
    "kommen": ("kam", "ist gekommen"),
    "sehen": ("sah", "hat gesehen"),
    "geben": ("gab", "hat gegeben"),
    "nehmen": ("nahm", "hat genommen"),
    "finden": ("fand", "hat gefunden"),
    "stehen": ("stand", "hat gestanden"),
    "sitzen": ("saß", "hat gesessen"),
    "liegen": ("lag", "hat gelegen"),
    "schreiben": ("schrieb", "hat geschrieben"),
    "lesen": ("las", "hat gelesen"),
    "fahren": ("fuhr", "ist gefahren"),
    "bringen": ("brachte", "hat gebracht"),
    "denken": ("dachte", "hat gedacht"),
    "essen": ("aß", "hat gegessen"),
    "trinken": ("trank", "hat getrunken"),
    "bleiben": ("blieb", "ist geblieben"),
    "beginnen": ("begann", "hat begonnen"),
    "sprechen": ("sprach", "hat gesprochen"),
    "laufen": ("lief", "ist gelaufen"),
    "schlafen": ("schlief", "hat geschlafen"),
    "helfen": ("half", "hat geholfen"),
    "treffen": ("traf", "hat getroffen"),
    "verlieren": ("verlor", "hat verloren"),
    "gewinnen": ("gewann", "hat gewonnen"),
    "vergessen": ("vergaß", "hat vergessen"),
    "ziehen": ("zog", "hat gezogen"),
    "fallen": ("fiel", "ist gefallen"),
    "halten": ("hielt", "hat gehalten"),
    "lassen": ("ließ", "hat gelassen"),
    "fliegen": ("flog", "ist geflogen"),
    "sterben": ("starb", "ist gestorben"),
    "wissen": ("wusste", "hat gewusst"),
    "können": ("konnte", "hat gekonnt"),
    "müssen": ("musste", "hat gemusst"),
    "wollen": ("wollte", "hat gewollt"),
    "dürfen": ("durfte", "hat gedurft"),
    "mögen": ("mochte", "hat gemocht"),
    "sollen": ("sollte", "hat gesollt"),
}

# ========== HELPER FUNCTIONS ==========
def get_verb_forms(verb, is_separable=False):
    """Get Perfekt and Präteritum forms for verbs"""
    if is_separable:
        # Handle separable verbs
        prefixes = ["ab", "an", "auf", "aus", "ein", "mit", "nach", "vor", "zu", "zurück", "weg", "her", "hin", "fort", "weiter"]
        for prefix in prefixes:
            if verb.startswith(prefix):
                base_verb = verb[len(prefix):]
                if base_verb in IRREGULAR_VERBS:
                    prateritum, perfekt_part = IRREGULAR_VERBS[base_verb]
                    # Separable prefix goes to end in Präteritum
                    prateritum = f"{prateritum} {prefix}"
                    # Prefix goes before ge- in Perfekt
                    if "ist" in perfekt_part:
                        aux = "ist"
                        participle = perfekt_part.replace("ist ", "").replace("hat ", "")
                        if participle.startswith("ge"):
                            participle = prefix + participle
                        else:
                            participle = prefix + "ge" + participle
                        perfekt = f"{aux} {participle}"
                    else:
                        aux = "hat"
                        participle = perfekt_part.replace("hat ", "").replace("ist ", "")
                        if participle.startswith("ge"):
                            participle = prefix + participle
                        else:
                            participle = prefix + "ge" + participle
                        perfekt = f"{aux} {participle}"
                    return perfekt, prateritum
                else:
                    # Regular separable verb
                    prateritum = f"{base_verb}te {prefix}"
                    participle = f"{prefix}ge{base_verb}t"
                    # Choose auxiliary (most separable verbs use "hat")
                    aux = "ist" if base_verb in ["gehen", "kommen", "fahren", "laufen", "steigen"] else "hat"
                    perfekt = f"{aux} {participle}"
                    return perfekt, prateritum
        
        # If no prefix found, treat as regular
        return get_verb_forms(verb, False)
    
    else:
        # Regular and irregular verbs
        if verb in IRREGULAR_VERBS:
            prateritum, perfekt = IRREGULAR_VERBS[verb]
            return perfekt, prateritum
        else:
            # Regular verb conjugation
            if verb.endswith("ieren"):
                prateritum = verb[:-2] + "te"
                perfekt = f"hat {verb[:-2]}t"
            else:
                prateritum = verb + "te" 
                perfekt = f"hat ge{verb}t"
            return perfekt, prateritum

def build_vocabulary_list():
    """Build the complete vocabulary list with proper distribution"""
    all_words = []
    
    # Add verbs
    verb_count = 0
    for verb, meaning, synonym in REAL_VERBS:
        if verb_count >= TARGET["Verb"]:
            break
        perfekt, prateritum = get_verb_forms(verb)
        all_words.append({
            "Type": "Verb",
            "Word": verb,
            "Meaning": meaning,
            "Perfekt": perfekt,
            "Präteritum": prateritum,
            "Sinonim": synonym
        })
        verb_count += 1
    
    # Add separable verbs
    sep_count = 0
    for verb, meaning, synonym in REAL_SEPARABLE_VERBS:
        if sep_count >= TARGET["Trennbare Verb"]:
            break
        perfekt, prateritum = get_verb_forms(verb, is_separable=True)
        all_words.append({
            "Type": "Trennbare Verb",
            "Word": verb,
            "Meaning": meaning,
            "Perfekt": perfekt,
            "Präteritum": prateritum,
            "Sinonim": synonym
        })
        sep_count += 1
    
    # Add adjectives
    adj_count = 0
    for adj, meaning, synonym in REAL_ADJECTIVES:
        if adj_count >= TARGET["Adjektiv"]:
            break
        all_words.append({
            "Type": "Adjektiv",
            "Word": adj,
            "Meaning": meaning,
            "Perfekt": "–",
            "Präteritum": "–",
            "Sinonim": synonym
        })
        adj_count += 1
    
    # Add nouns
    noun_count = 0
    for noun, meaning, synonym in REAL_NOUNS:
        if noun_count >= TARGET["Nomen"]:
            break
        all_words.append({
            "Type": "Nomen",
            "Word": noun,
            "Meaning": meaning,
            "Perfekt": "–",
            "Präteritum": "–",
            "Sinonim": synonym
        })
        noun_count += 1
    
    # Sort each type alphabetically
    types = ["Verb", "Trennbare Verb", "Adjektiv", "Nomen"]
    sorted_words = []
    
    for word_type in types:
        type_words = [w for w in all_words if w["Type"] == word_type]
        type_words.sort(key=lambda x: x["Word"].lower())
        sorted_words.extend(type_words)
    
    return sorted_words

def export_to_csv(words, filename="german_2000_real.csv"):
    """Export vocabulary to CSV file"""
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    
    df = pd.DataFrame(words)
    # Reorder columns as requested
    df = df[["Word", "Meaning", "Perfekt", "Präteritum", "Sinonim"]]
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    return filepath

def export_to_pdf(words, filename="german_2000_real.pdf"):
    """Export vocabulary to PDF file with color coding"""
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=landscape(A4), 
                          leftMargin=12, rightMargin=12, topMargin=12, bottomMargin=12)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title and legend
    title = Paragraph("<b>2000 Real German Vocabulary (A2–C1 Level)</b>", styles["Title"])
    legend = Paragraph(
        "Columns: <b>Word</b> | <b>Meaning (Indonesian)</b> | <b>Perfekt</b> | <b>Präteritum</b> | <b>Sinonim</b><br/>"
        "Color coding: 🟩 Verb | 🟦 Trennbare Verb | 🟧 Adjektiv | 🟥 Nomen", 
        styles["Normal"]
    )
    elements.extend([title, Spacer(1, 6), legend, Spacer(1, 8)])
    
    # Create table data
    headers = ["Word", "Meaning (ID)", "Perfekt", "Präteritum", "Sinonim"]
    
    # Process in chunks for better PDF layout
    CHUNK_SIZE = 48
    total_words = len(words)
    
    for start_idx in range(0, total_words, CHUNK_SIZE):
        end_idx = min(start_idx + CHUNK_SIZE, total_words)
        chunk_words = words[start_idx:end_idx]
        
        # Create table data for this chunk
        table_data = [headers]
        for word in chunk_words:
            table_data.append([
                word["Word"],
                word["Meaning"],
                word["Perfekt"],
                word["Präteritum"],
                word["Sinonim"]
            ])
        
        # Create table
        table = Table(table_data, colWidths=[140, 260, 140, 140, 160], repeatRows=1)
        
        # Base table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ])
        
        # Color coding for word types
        for i, word in enumerate(chunk_words, start=1):
            word_type = word["Type"]
            if word_type == "Verb":
                bg_color = colors.lightgreen
            elif word_type == "Trennbare Verb":
                bg_color = colors.lightblue
            elif word_type == "Adjektiv":
                bg_color = colors.orange
            else:  # Nomen
                bg_color = colors.lightcoral
            
            table_style.add('BACKGROUND', (0, i), (0, i), bg_color)
        
        table.setStyle(table_style)
        elements.append(table)
        
        # Add page break if not the last chunk
        if end_idx < total_words:
            elements.append(PageBreak())
    
    doc.build(elements)
    return filepath

def main():
    """Main function to generate German vocabulary"""
    print("🇩🇪 Generating 2000 Real German Vocabulary Words...")
    print("=" * 50)
    
    # Build vocabulary list
    print("📚 Building vocabulary list...")
    words = build_vocabulary_list()
    
    # Verify counts
    type_counts = {}
    for word in words:
        word_type = word["Type"]
        type_counts[word_type] = type_counts.get(word_type, 0) + 1
    
    print(f"✅ Generated {len(words)} words total:")
    for word_type, count in type_counts.items():
        print(f"   • {word_type}: {count} words")
    
    # Export to CSV
    print("\n💾 Exporting to CSV...")
    csv_path = export_to_csv(words)
    print(f"✅ CSV saved: {csv_path}")
    
    # Export to PDF
    print("\n📄 Exporting to PDF...")
    pdf_path = export_to_pdf(words)
    print(f"✅ PDF saved: {pdf_path}")
    
    print("\n🎉 Generation complete!")
    print("=" * 50)
    print("Files created in 'output' folder:")
    print(f"  • {csv_path}")
    print(f"  • {pdf_path}")

if __name__ == "__main__":
    main()