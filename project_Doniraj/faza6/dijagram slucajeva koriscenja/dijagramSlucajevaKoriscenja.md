```mermaid
flowchart TD
    Guest[Gost] --> RegistracijaKaoKorisnik
    Guest --> RegistracijaKaoOrganizacija
    Guest --> PregledOglasa
    Guest --> PregledPojedinacnogOglasa
    Guest --> PregledOrganizacija
    Guest --> PregledPojedinacneOrganizacije
    Guest --> PregledPojedinacnogProfila
    Guest --> OporavakLozinke    

    subgraph Slučajevi korišćenja gosta
        RegistracijaKaoKorisnik[Registracija kao korisnik]
        RegistracijaKaoOrganizacija[Registracija kao organizacija]
        PregledOglasa[Pregled svih oglasa]
        PregledPojedinacnogOglasa[Pregled pojedinacnog oglasa]
        PregledOrganizacija[Pregled svih organizacija]
        PregledPojedinacneOrganizacije[Pregled pojedinacne organizacije]
        PregledPojedinacnogProfila[Pregled profila registrovanog korisnika]
        OporavakLozinke[Oporavak lozinke]
    end
```

```mermaid
flowchart TD
    User[Registrovani Obican Korisnik] --> Prijava
    User --> Odjava
    User --> PregledOglasa
    User --> PregledPojedinacnogOglasa
    User --> PregledOrganizacija
    User --> PregledPojedinacneOrganizacije
    User --> PregledPojedinacnogProfila
    User --> PravljenjeOglasa
    User --> BrisanjeOglasa
    User --> PromenaLozinke
    User --> PromenaProfilneSlike
    User --> PregledSopstvenogProfila
    User --> KontaktiranjeDrugogKorisnika
    User --> PregledInboxa
    
    subgraph Slučajevi korišćenja registrovanog korisnika 
        PregledOglasa[Pregled svih oglasa]
        PregledPojedinacnogOglasa[Pregled pojedinacnog oglasa]
        PregledOrganizacija[Pregled svih organizacija]
        PregledPojedinacneOrganizacije[Pregled pojedinacne organizacije]
        PregledPojedinacnogProfila[Pregled profila obicnog korisnika]
        
        PravljenjeOglasa[Pravljenje oglasa za doniranje]
        BrisanjeOglasa[Brisanje sopstvenog oglasa za doniranje]
        PromenaLozinke[Promena lozinke]
        PromenaProfilneSlike[Promena profilne slike]
        PregledSopstvenogProfila[Pregled sopstvenog profila]
        KontaktiranjeDrugogKorisnika[Kontaktiranje drugog korisnika]
        PregledInboxa[Pregled inboxa]
        Prijava[Prijava]
        Odjava[Odjava]
    end
```


```mermaid
flowchart TD
    User[Registrovana Organizacija] --> Prijava
    User --> Odjava
    User --> PregledOglasa
    User --> PregledPojedinacnogOglasa
    User --> PregledOrganizacija
    User --> PregledPojedinacneOrganizacije
    User --> PregledPojedinacnogProfila
    User --> PromenaLozinke
    User --> PromenaProfilneSlike
    User --> PregledSopstvenogProfila
    User --> KontaktiranjeDrugogKorisnika
    User --> PregledInboxa
    
    subgraph Slučajevi korišćenja registrovane organizacije
        PregledOglasa[Pregled svih oglasa]
        PregledPojedinacnogOglasa[Pregled pojedinacnog oglasa]
        PregledOrganizacija[Pregled svih organizacija]
        PregledPojedinacneOrganizacije[Pregled pojedinacne organizacije]
        PregledPojedinacnogProfila[Pregled profila obicnog korisnika]
        
        PromenaLozinke[Promena lozinke]
        PromenaProfilneSlike[Promena profilne slike]
        PregledSopstvenogProfila[Pregled sopstvenog profila]
        KontaktiranjeDrugogKorisnika[Kontaktiranje drugog korisnika]
        PregledInboxa[Pregled inboxa]
        Prijava[Prijava]
        Odjava[Odjava]
    end
```

```mermaid
flowchart TD
    Admin[Administrator] --> Prijava
    Admin --> Odjava
    Admin --> PregledOglasa
    Admin --> PregledPojedinacnogOglasa
    Admin --> PregledOrganizacija
    Admin --> PregledPojedinacneOrganizacije
    Admin --> PregledPojedinacnogProfila
    Admin --> BrisanjeOglasaKorisnika
    Admin --> BrisanjeNaloga
    Admin --> PromenaLozinke
    Admin --> PromenaProfilneSlike
    Admin --> PregledSopstvenogProfila
    Admin --> KontaktiranjeDrugogKorisnika
    Admin --> PregledInboxa
    Admin --> OdobravanjeOrganizacija
    
    subgraph Slučajevi korišćenja administratora
        PregledOglasa[Pregled svih oglasa]
        PregledPojedinacnogOglasa[Pregled pojedinacnog oglasa]
        PregledOrganizacija[Pregled svih organizacija]
        PregledPojedinacneOrganizacije[Pregled pojedinacne organizacije]
        PregledPojedinacnogProfila[Pregled profila obicnog korisnika]
        
        BrisanjeOglasaKorisnika[Brisanje oglasa za doniranje]
        BrisanjeNaloga[Brisanje naloga]
        PromenaLozinke[Promena lozinke]
        PromenaProfilneSlike[Promena profilne slike]
        PregledSopstvenogProfila[Pregled sopstvenog profila]
        KontaktiranjeDrugogKorisnika[Kontaktiranje drugog korisnika]
        PregledInboxa[Pregled inboxa]

        OdobravanjeOrganizacija[Odobravanje organizacija]
        Prijava[Prijava]
        Odjava[Odjava]
    end
```