# Fonts

`python scripts/fetch_fonts.py --all` downloads the licence-safe set here (all OFL, free for
commercial use). `--urdu` fetches only the Urdu/Arabic faces. `--list` shows every key.

**Display (headlines):** Anton, Bebas Neue, Archivo Black, Montserrat (variable),
Poppins ExtraBold/Black, Oswald (variable), Teko (variable), Barlow Condensed ExtraBold.
**UI / support:** Inter (variable).
**Urdu / Arabic:** Noto Nastaliq Urdu, Noto Naskh Arabic, Lateef.

`base.css` declares each face with a `local()` fallback first, so a font already installed on
the system is used before the file here.

## Do not add without a licence
Impact (system-only), Gilroy, Akira Expanded, Jameel Noori Nastaleeq, and any other paid
family. If the user owns a licence, drop the file here and name it in the delivery note -
otherwise substitute the nearest OFL face and say which one you used.
