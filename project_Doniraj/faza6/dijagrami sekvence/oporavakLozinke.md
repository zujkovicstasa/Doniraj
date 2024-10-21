```mermaid
sequenceDiagram
    actor Gost
    participant Template
    participant View
    participant Model
    participant Database
    participant Email service
    
    Gost ->> Template: Klik na dugme "Uloguj se" 
    View -->> Template: Prikaz stranice za login
    Template -->> Gost: Prikaz stranice za login
    Gost ->> Template: Klik na dugme "Zaboravili ste lozinku?"
    View -->> Template: Prikaz forme za unos email-a
    Template -->> Gost: Prikaz forme za unos email-a
    Gost ->> Template: Unos email-a
    Template ->> View: Pošalji uneseni email
    alt email nije unet
        View -->> Template: Prikaz poruke da je email obavezan
        Template -->> Gost: Prikaz poruke da je email obavezan
    else else
        View ->> Model: Pronadji korisnika sa datim email-om
        Model ->> Database: Pronadji korisnika sa datim email-om
        alt Korisnik sa datim email-om nije pronadjen
            Database -->> Model: Korisnik sa datim email-om nije pronadjen
            Model -->> View: Korisnik sa datim email-om nije pronadjen
            View -->> Template: Prikaz poruke o nevalidnom email-u
            Template -->> Gost: Prikaz poruke o nevalidnom email-u
        else else
            Database -->> Model: Korisnik sa datim email-om postoji
            Model -->> View: Korisnik sa datim email-om postoji
            View ->> Email service: Posalji kod na email
            View ->> Template: Prikaz sledeceg koraka (verifikacija mejla)
            Template ->> Gost: Prikaz forme za unos koda poslatog na mejl
            Gost -->> Template: Unos koda
            Template -->> View: Proveri kod
            alt Kod nije unet
                View ->> Template: Prikaz poruke da je kod obavezan
                Template ->> Gost: Prikaz poruke da je kod obavezan
            else Kod nije validan
                View ->> Template: Prikaz poruke o nevalidnom kodu
                Template ->> Gost: Prikaz poruke o nevalidnom kodu
            else Kod je validan
                View ->> Template: Prikaz sledeceg koraka (promena lozinke)
                Template ->> Gost: Prikaz forme promene lozinke
                Gost -->> Template: Unos nove lozinke i nove ponovljene lozinke
                Template -->> View: Proveri lozinku i ponovljenu lozinku
                alt Neko polje nije uneto
                    View ->> Template: Prikaz poruke da su sva polja obavezna
                    Template ->> Gost: Prikaz poruke da su sva polja obavezna
                else Lozinke se ne poklapaju
                    View ->> Template: Prikaz poruke da se lozinke ne poklapaju
                    Template ->> Gost: Prikaz poruke da se lozinke ne poklapaju
                else Lozinke se poklapaju
                    View ->> Model: Promeni lozinku datom korisniku
                    Model ->> Database: Promeni lozinku datom korisniku
                    Database -->> Model: Lozinka promenjena
                    Model -->> View: Lozinka promenjena
                    View -->> Template: Lozinka promenjena, prebaci na login stranicu
                    Template -->> Gost: Lozinka uspesno promenjena, prikaz login stranice
                end
            end
        end
    end
```

