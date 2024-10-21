
//Author:Marija Stakic 2021/0320
function toggleFields(tip) {
    if (tip === 'korisnik') {
        document.getElementById('organizacijaFields').style.display = 'none';
    } else if (tip === 'organizacija') {
        document.getElementById('organizacijaFields').style.display = 'block';
    }
}





