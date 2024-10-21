```mermaid
sequenceDiagram
    actor Gost
    participant Template
    participant View
    participant Model
    participant Database

    Gost ->> Template: Gost pritiska profilnu sliku korisnika
    Template ->> View: Zahteva kreiranje pregleda profila
    View ->> Model: Zahteva podatke o korisniku
    Model ->> Database: Trazi podatke o korisniku preko id-ja
    alt Korisnik na ciji je profil kliknuto ne postoji 
        Database -->> Model: Ne pronalazi podatke
        Model -->> View: Ne postoji korisnik
        View -->> Template: Izbacuje gresku 404
        Template -->> Gost: Stranica ne moze da se kreira, ispisuje se greska
    else Korisnik postoji
        Database -->> Model: Vraca podatke o korisniku
        Model -->> View: Vraca Korisnika
        View ->> Model: Salje zahtev za oglase datog korisnika
        Model ->> Database: Trazi svaki oglas iz baze za korisnika sa zadatim id-jem
        Database -->> Model: Vraca sve pronadjene oglase
        Model -->> View: Vraca sve pronadjene oglase
        View ->> Template: Kreiranje stranice za pregled profila korisnika sa svim oglasima
        Template ->> Gost: Prikaz stranice za pregled profila korisnika
    end

    
    
```