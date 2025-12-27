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