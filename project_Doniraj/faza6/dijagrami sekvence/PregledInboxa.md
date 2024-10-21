```mermaid
sequenceDiagram
    actor Korisnik
    participant Template
    participant View
    participant Model
    participant Database

    Korisnik->>Template: Korisnik pritiska na dugme inbox na pregledu sopstvenog profila
    Template->>View: Zahteva kreiranje inbox stranice
    View->>Model: Zahteva kreirane privatne chatove sa korisnicima
    Model->>Database: Zahteva kreirane privatne chatove sa korisnicima
    Database-->>Model: Vraca sve chatove zadatog korisnika
    Model-->>View: Vraca sve chatove zadatog korisnika
    View-->>Template: Vraca sortirane chatove i salje zahtev za kreiranje stranice
    loop For chat in sortirani chatovi
        Template->>Model: Trazi informaciju o chatu
        Model->>Database: Trazi Korisnika koji je u chatu kao i poslednju poslatu poruku
        Database-->>Model: Vraca Korisnika koji je u chatu i poslednju poslatu poruku
        Model-->>Template: Vraca podatke o chatu
    end
    
    Template->>Korisnik: Prikaz inbox stranice
    
    
```