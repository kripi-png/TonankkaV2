## Discord Application

[https://discord.com/developers/applications](https://discord.com/developers/applications)
1. Paina New Application -nappia
2. Anna botille nimi (ie. testibotti)
3. Valitse sivuvalikosta Bot ja paina Add Bot -nappia
4. Voit halutessasi klikata PUBLIC BOT -option pois päältä, mutta tämän ei pitäisi vaikuttaa mihinkään.
5. Huomaa Copy-nappi Token-otsikon alla. Tulet tarvitsemaan botin tokenia (periaatteess käyttäjänimi ja salasana yhtenä pitkänä merkkijonona) myöhemmin ja sen saa painamalla kyseistä nappia. Tokenia ei saa jakaa muille, aivan kuten et jakaisi omia salasanojasikaan.
6. Valitse sivuvalikosta OAuth2. Valitse Scopes-listasta bot ja Bot Permissions-kohdasta Administrator. Kopioi linkki listojen välissä ja liitä se osoitepalkkiin. Valitse serveri, jossa haluat bottiasi testata. Voit luoda oman serverin melko helposti ja nopeasti Discordin sovelluksessa* Paina Continue ja sen jälkeen Authorize.
7. Serverin luodaksesi, paina Discordin server-listan lopusta +-nappia ja seuraa ohjeita. Mut voi myös invitee sinne myöhemmin jos tulee jotain ongelmia.


## Github ja botin koodi
1. Mene osoitteeseen https://git-scm.com/downloads ja lataa git (oletettavasti) Windowsille. Asenna.
2. Kun Git on asennettu, avaa komentokehote joko hakemalla Windowsin haku-toiminnolla tai painamalla win + R ja kirjoittamalla cmd avautuvaan kenttään.
3. Navigoi työpöydällesi kirjoittamalla komentokehoitteeseen ```cd Desktop```
4. Kirjoita/copy&paste komentokehoitteeseen seuraava rivi:
```bash
git clone https://github.com/kripi-png/TonankkaV2.git
```
5. Työpöydälläsi pitäisi nyt olla kansio nimeltä TonankkaV2.
6. Kirjoita komentokehoitteeseen ```cd TonankkaV2```.
4. Kirjoita kenttään seuraava rivi ja paina enteriä jälkeen:
```bash
py -3 -m pip install -U discord.py
```
5. Kirjoita komentokehoitteeseen ```notepad botToken.py``` (case-sensitive) ja vahvista tiedoston luominen.
6. Käy kopioimassa bottisi token (katso Discord Application -osaa jos et muista miten)
7. Kirjoita avattuun notepad-ikkunaan seuraava:
```
token = "copy/paste bot token tähän"
```
8. Tallenna tiedosto.
9. Kirjoita komentokehoitteeseen ```py -3 main.py``` käynnistääksesi botin. Jos ja kun komentokehoitteeseen ilmestyy rivi ```We have logged in as [nimi#discriminator]```, tiedät botin toimivan. Voit nyt mennä serverillesi ja testata bottia komennolla ```!ping```.
10. Sammuttaaksesi botin, paina CTRL + C ollessasi komentokehoitteessa. Voit käynnistää sen uudelleen komennolla ```py -3 main.py```
11. Voit nyt muokata tiedostoja haluamasi mukaan. Luodaksesi uuden komennon, voit kopioida esimerkiksi ping.py-tiedoston ja nimetä sen uudelleen. @woope jos tulee ongelmia.
