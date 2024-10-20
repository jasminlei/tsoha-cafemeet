Lounasseurasovellus

Sovelluksen tarkoituksena on toimia apuvälineenä lounasseuran löytämiseen. Sen avulla käyttäjät voivat helposti tarkistaa, milloin heidän kaverinsa ovat saatavilla lounaalle, tai tutustua uusiin ihmisiin yhteisen lounaan merkeissä.  


Tällä hetkellä toiminnassa olevat ominaisuudet: 

- Sovellukseen voi luoda käyttäjän ja kirjautua sisään. 
- Rekisteröityneet käyttäjät näkyvät etusivulla. 
- Kirjautunut käyttäjä voi muokata omaa profiiliaan. 
- Käyttäjä voi lähettää muille käyttäjille kaveripyynnön ja hyväksyä muiden käyttäjien lähettämiä kaveripyyntöjä. 
- Käyttäjä voi luoda omia lounasilmoituksia, ja tarkastella muiden lounasilmoituksia.
- Ilmoituksen voi asettaa julkiseksi tai näkymään vain kavereille. 
- Etusivulla näytetään kolme uusinta lounasilmoitusta. 
- Käyttäjä voi kommentoida muiden lounasilmoituksia, ja lukea muiden kommentteja ilmoituksissa.



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

