const locations = [
  { name: "Snoopy Island", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Shark Island", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Anemone Gardens", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Dibba Island", region: "Fujairah", country: "UAE" },
  { name: "Martini Rock", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Inchcape 1 Wreck", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Inchcape 2 Wreck", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Martini Wall", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Snoopy Deep Reef", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Artificial Reef", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Coral Gardens", region: "Fujairah, Al Aqah", country: "UAE" },

  { name: "Daymaniyat Islands (Three Sisters)", region: "Daymaniyat Islands", country: "Oman" },
  { name: "Musandam Fjords", region: "Musandam, Khasab", country: "Oman" },
  { name: "Bandar Khayran", region: "Muscat", country: "Oman" },

  { name: "Ningaloo Reef", region: "Western Australia", country: "Australia" },
  { name: "Darwin Island", region: "Galapagos", country: "Ecuador" },
  { name: "Tofo", region: "Inhambane Province", country: "Mozambique" },
  { name: "Hanifaru Bay", region: "Baa Atoll", country: "Maldives" },
  { name: "Socorro Island", region: "Revillagigedo Islands", country: "Mexico" },
  { name: "Tiger Beach", region: "Grand Bahama", country: "Bahamas" },
  { name: "Aliwal Shoal", region: "KwaZulu-Natal", country: "South Africa" },
  { name: "Brothers Islands", region: "Red Sea", country: "Egypt" },
  { name: "Blue Corner", region: "Koror", country: "Palau" },
  { name: "Monad Shoal", region: "Malapascua", country: "Philippines" },
  { name: "Sipadan Island", region: "Sabah", country: "Malaysia" },
  { name: "Barracuda Point", region: "Sabah", country: "Malaysia" },
  { name: "Turtle City", region: "Gili Islands", country: "Indonesia" },
  { name: "Manta Point", region: "Komodo National Park", country: "Indonesia" },
  { name: "Crystal Bay", region: "Nusa Penida", country: "Indonesia" },
  { name: "Cape Kri", region: "Raja Ampat", country: "Indonesia" },
  { name: "Lembeh Strait", region: "North Sulawesi", country: "Indonesia" },
  { name: "Poor Knights Islands", region: "Northland", country: "New Zealand" },
  { name: "Tubbataha Reefs", region: "Sulu Sea", country: "Philippines" },
  { name: "San Carlos Beach", region: "Monterey, California", country: "USA" },
  { name: "Monterey Bay", region: "California", country: "USA" },
  { name: "Madrona Point", region: "British Columbia", country: "Canada" }
];

locations.sort((a, b) => a.country.localeCompare(b.country));

const locationSelect = document.getElementById("location");

locations.forEach(loc => {
  const option = document.createElement("option");
  option.value = `${loc.name}, ${loc.region}, ${loc.country}`;
  option.textContent = `${loc.name}, ${loc.region}, ${loc.country}`;
  locationSelect.appendChild(option);
});

document.getElementById("submitBtn").addEventListener("click", async () => {
  const location = document.getElementById("location").value;
  const day = document.getElementById("day").value;
  const time = document.getElementById("time").value;
  const loader = document.getElementById("loader");
  const resultContainer = document.getElementById("result-container");
  const resultText = document.getElementById("result-text");

  if (!location || !day || !time) {
    alert("Please fill all fields");
    return;
  }

  resultText.innerHTML = "";
  resultContainer.style.display = "none";
  loader.style.display = "block";

  try {
    const response = await fetch("http://localhost:8080/analyse-dive", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location, date: day, time })
    });

    const data = await response.json();
    loader.style.display = "none";

    if (data.error) {
      resultText.innerHTML = `<div class='error'>${data.error}</div>`;
    } else {
      resultText.textContent = data.llm_response;
    }

    resultContainer.style.display = "block";
  } catch (err) {
    loader.style.display = "none";
    resultText.innerHTML = "<div class='error'>Server error. Please try again later.</div>";
    resultContainer.style.display = "block";
  }
});
