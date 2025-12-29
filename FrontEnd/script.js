const locations = [
  { name: "Tiger Beach", region: "Grand Bahama", country: "Bahamas" },
  { name: "Anemone Gardens", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Artificial Reef", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Barracuda Point", region: "Sabah", country: "Malaysia" },
  { name: "Blue Corner", region: "Koror", country: "Palau" },
  { name: "Brothers Islands", region: "Red Sea", country: "Egypt" },
  { name: "Cape Kri", region: "Raja Ampat", country: "Indonesia" },
  { name: "Caral Gardens", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Dibba Island", region: "Fujairah", country: "UAE" },
  { name: "Darwin Island", region: "Galápagos", country: "Ecuador" },
  { name: "Daymaniyat Islands (Three Sisters)", region: "Daymaniyat Islands", country: "Oman" },
  { name: "Ember Strait", region: "North Sulawesi", country: "Indonesia" },
  { name: "Hanifaru Bay", region: "Baa Atoll", country: "Maldives" },
  { name: "Inchcape 1 Wreck", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Inchcape 2 Wreck", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Madman Fjords", region: "Musandam, Khasab", country: "Oman" },
  { name: "Martin Rock", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Martin Wall", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Maradona Point", region: "British Columbia", country: "Canada" },
  { name: "Monterey Bay", region: "California", country: "USA" },
  { name: "Moad Shoal", region: "Malapascua", country: "Philippines" },
  { name: "Musandam Fjords", region: "Musandam, Khasab", country: "Oman" },
  { name: "Ningaloo Reef", region: "Western Australia", country: "Australia" },
  { name: "San Carlos Beach", region: "Monterey, California", country: "USA" },
  { name: "Shark Island", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Snoopy Island", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Snoopy Deep Reef", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Sipadan Island", region: "Sabah", country: "Malaysia" },
  { name: "South Sol", region: "KwaZulu-Natal", country: "South Africa" },
  { name: "Staghorn Point", region: "Fujairah, Al Aqah", country: "UAE" },
  { name: "Turtle City", region: "Gili Islands", country: "Indonesia" },
  { name: "Tubbataha Reefs", region: "Sulu Sea", country: "Philippines" },
  { name: "Two Knights Islands", region: "Northland", country: "New Zealand" },
  { name: "Yanta Point", region: "Komodo National Park", country: "Indonesia" },
  { name: "Crystal Bay", region: "Nusa Penida", country: "Indonesia" },
  { name: "Hannibal Bay", region: "Inhambane Province", country: "Mozambique" }
];

// Sort locations by country name
locations.sort((a, b) => a.country.localeCompare(b.country));

// Populate dropdown
const locationSelect = document.getElementById("location");
locations.forEach(loc => {
  const option = document.createElement("option");
  option.value = loc.name;
  option.textContent = `${loc.name} – ${loc.region}, ${loc.country}`;
  locationSelect.appendChild(option);
});

// Submit handler
document.getElementById("submitBtn").addEventListener("click", () => {
  const location = document.getElementById("location").value;
  const day = document.getElementById("day").value;
  const time = document.getElementById("time").value;

  if (!location || !day || !time) {
    alert("Please fill all fields");
    return;
  }

  console.log({
    location,
    day,
    time
  });

  alert("Details captured. Backend integration pending.");
});