```mermaid
sequenceDiagram
    actor Admin
    participant Template
    participant View
    participant Model
    participant Database
    
    Admin ->> Template: Klik na odredjeni profil korisnika 
    View -->> Template: Prikaz stranice korisnika sa njegovim oglasima
    Template -->> Admin: Prikaz stranice korisnika sa njegovim oglasima
    Admin ->> Template: Klik na dugme "Obrisi oglas"
    Template ->> View: Obrisi oglas sa datim id-em
    View ->> Model: Pronadji oglas sa datim id-em
    Model ->> Database: Pronadji oglas sa datim id-em

    alt Oglas sa datim id-em ne postoji
        Database -->> Model: Oglas ne postoji
        Model -->> View: Oglas ne postoji
        View -->> Template: Prikaz 404 stranice
        Template -->> Admin: Prikaz 404 stranice
    else else
        Database -->> Model: Oglas
        Model -->> View: Oglas
        View ->> Model: Pronadji sve tagove vezane za ovaj oglas
        Model ->> Database: Pronadji sve tagove vezane za ovaj oglas
        Database -->> Model: Tagovi
        Model -->> View: Tagovi
        View ->> Model: Izbrisi oglas
        Model ->> Database: Izbrisi oglas
        Database -->> Model:  Oglas obrisan
        Model -->> View:  Oglas obrisan
        loop for tag in tagovi
            View ->> Model: Proveri da li postoji neki oglas vezan za ovaj tag
            Model ->> Database: Proveri da li postoji neki oglas vezan za ovaj tag
            alt ne postoji
                Database -->> Model: ne postoji
                Model -->> View: ne postoji
                View ->> Model: Obrisi tag
                Model ->> Database: Obrisi tag
                Database -->> Model: tag obrisan
                Model -->> View: tag obrisan
            end
        end
        View ->> Template: Oglas Obrisan
        Template ->> Admin: prikaz poruke o obrisanom oglasu
    end
```

