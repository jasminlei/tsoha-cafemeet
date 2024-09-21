Lounasseurasovellus

Sovelluksen tarkoituksena on toimia apuvälineenä lounasseuran löytämiseen. Sen avulla käyttäjät voivat helposti tarkistaa, milloin heidän kaverinsa ovat saatavilla lounaalle, tai tutustua uusiin ihmisiin yhteisen lounaan merkeissä.  

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.

Käyttäjä voi lisätä toisia käyttäjiä kaveriksi.

Käyttäjä voi lisätä julkisen ilmoituksen, tai ilmoituksen joka näkyy vain kavereille. Ilmoitukseen voi valita haluamansa Unicafen tai kampuksen sekä kellonajan.

Käyttäjä voi poistaa ilmoituksensa tai muokata sitä.

Käyttäjä voi hakea muiden ilmoituksia tietyn lounasravintolan, kampuksen tai kellonajan perusteella.

Käyttäjä voi kommentoida muiden ilmoituksia.

Käyttäjä voi lähettää yksityisviestejä toisille käyttäjille. 


Tällä hetkellä toimivat ominaisuudet: 

- Sovellukseen voi luoda käyttäjän ja kirjautua sisään 
- Kirjautunut käyttäjä voi muokata omaa profiiliaan 
- Kirjautunut käyttäjä voi vierailla muiden käyttäjien profiileissa 
- Käyttäjä voi lähettää muille käyttäjille kaveripyynnön ja hyväksyä muiden käyttäjien lähettämiä kaveripyyntöjä 


Käynnistysohjeet: 


Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi: 

```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```


Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla: 

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```


Määritä tietokannan skeema komennolla: 

```
$ psql < schema.sql
```


Käynnistä sovellus komennolla: 

```
$ flask run
```

