function popuniStranicu(n) {
  let artikli = document.getElementById("artikli");

  for (let i = 1; i <= n; i++) {
    let link = document.createElement("a");
    link.href = "pojedinacan.html";

    let kartica = document.createElement("div");
    kartica.className = "card";
    kartica.style.width = "18rem";

    let slika = document.createElement("img");
    slika.src = "images/artikal_1.png";
    slika.alt = "Proizvod";
    slika.className = "card-img-top";

    let telo = document.createElement("div");
    telo.className = "card-body";

    let tekst = document.createElement("p");
    tekst.className = "card-text";
    tekst.textContent = "veličina - stanje";
    let naziv = document.createElement("h4");
    naziv.textContent = "Naziv";

    telo.appendChild(naziv);
    telo.appendChild(tekst);
    kartica.appendChild(slika);
    kartica.appendChild(telo);
    link.appendChild(kartica);
    artikli.appendChild(link);
  }
}
function popuniStranicuAdmin(n) {
  let artikli = document.getElementById("artikliAdmin");

  for (let i = 1; i <= n; i++) {
    let kartica = document.createElement("div");
    kartica.className = "card";
    kartica.style.width = "18rem";

    let slika = document.createElement("img");
    slika.src = "images/artikal_1.png";
    slika.alt = "Proizvod";
    slika.className = "card-img-top";

    let telo = document.createElement("div");
    telo.className = "card-body";

    let tekst = document.createElement("p");
    tekst.className = "card-text";
    tekst.textContent = "Naziv, veličina, stanje";

    let obrisilink = document.createElement("a");
    let iks = document.createElement("img");
    iks.src = "images/iks.png";
    iks.alt = "iks";
    iks.style.width = "20px";
    obrisilink.appendChild(iks);
    obrisilink.appendChild(document.createTextNode("Obrisi oglas"));
    obrisilink.className = "link-danger mt-2";

    obrisilink.addEventListener("click", function () {
      if (confirm("Da li ste sigurni da želite da obrišete oglas?")) {
        kartica.remove();
      }
    });

    telo.appendChild(tekst);
    telo.appendChild(obrisilink);
    kartica.appendChild(slika);
    kartica.appendChild(telo);
    artikli.appendChild(kartica);
  }
}

function preusmeriLogIn() {
  let email = document.getElementById("emailLog").value;
  let lozinka = document.getElementById("lozinkaLog").value;

  if (email.trim() === "" || lozinka.trim() === "") {
    alert("Molimo vas da unesete email i lozinku.");
    return;
  }

  if (email === "admin@example.com" && lozinka === "admin") {
    window.location.href = "admin.html";
  } else if (
    email === "organizacija@example.com" &&
    lozinka === "organizacija"
  ) {
    window.location.href = "organizacijaSopstveni.html";
  } else if (email === "korisnik@example.com" && lozinka === "korisnik") {
    window.location.href = "profil.html";
  } else {
    alert("Neispravni podaci!");
  }
  azurirajNavigaciju(role);
}

document.addEventListener("DOMContentLoaded", function () {
  let ikoniceUklanjanja = document.querySelectorAll(".ukloni-oglas");

  ikoniceUklanjanja.forEach(function (ikonica) {
    ikonica.addEventListener("click", function () {
      let oglasID = this.getAttribute("data-oglas-id");
      if (confirm("Da li ste sigurni da želite da obrišete oglas?")) {
        let karticaOglasa = this.closest(".card");
        karticaOglasa.style.display = "none";
        alert("Oglas je uspešno obrisan!");
      }
    });
  });
});

function inicijalizujProdavnicu(n) {
  popuniStranicu(n);
}
function inicijalizujProdavnicuAdmin(n) {
  popuniStranicuAdmin(n);
}

function toggleFields(tip) {
  if (tip === "korisnik") {
    document.getElementById("korisnikFields").style.display = "block";
    document.getElementById("organizacijaFields").style.display = "none";
  } else if (tip === "organizacija") {
    document.getElementById("organizacijaFields").style.display = "block";
    document.getElementById("korisnikFields").style.display = "none";
  }
}

function nextStep() {
  document.getElementById("step1").style.display = "none";
  document.getElementById("step2").style.display = "block";
}
function verifyCode() {
  document.getElementById("step2").style.display = "none";
  document.getElementById("step3").style.display = "block";
}
function obrisiNalog(element) {
  if (confirm("Da li ste sigurni da želite da obrišete nalog?")) {
    let karticaNaloga = element.closest(".card");
    karticaNaloga.style.display = "none";
    alert("Nalog je uspešno obrisan!");
  }
}
