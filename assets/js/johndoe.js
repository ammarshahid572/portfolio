/*!
=========================================================
* JohnDoe Landing page
=========================================================

* Copyright: 2019 DevCRUD (https://devcrud.com)
* Licensed: (https://devcrud.com/licenses)
* Coded by www.devcrud.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// protfolio filters
$(window).on("load", function () {
  var t = $(".portfolio-container");
  t.isotope({
    filter: ".new",
    animationOptions: {
      duration: 750,
      easing: "linear",
      queue: !1,
    },
  }),
    $(".filters a").click(function () {
      $(".filters .active").removeClass("active"), $(this).addClass("active");
      var i = $(this).attr("data-filter");
      return (
        t.isotope({
          filter: i,
          animationOptions: {
            duration: 750,
            easing: "linear",
            queue: !1,
          },
        }),
        !1
      );
    });
});

// Extract data from JSON and create tiles dynamically

const tilesContainer = document.getElementById("iot-container");

fetch('/device/data/collection1')
  .then(response => response.json()) // parse the JSON data
  .then(data => {
data.forEach((device) => {
  
  const tile = document.createElement("div");
  tile.classList.add("tile");
  const chipId = document.createElement("div");
  const chipIdValue = document.createElement("div");
  chipIdValue.classList.add("device-name");
  chipIdValue.textContent = device.name;
  tile.appendChild(chipId);
  tile.appendChild(chipIdValue);
  const dataKeys = Object.keys(device.sensors);
  dataKeys.forEach((key) => {
    const dataKey = document.createElement("div");
    dataKey.classList.add("key");
    dataKey.textContent = key.charAt(0).toUpperCase() + key.slice(1);
    const dataValue = document.createElement("div");
    dataValue.classList.add("value");

    dataValue.textContent = device.sensors[key];
    if  (device.units[key]) dataValue.textContent = dataValue.textContent +  device.units[key];
    tile.appendChild(dataKey);
    tile.appendChild(dataValue);
  });
  

  tilesContainer.appendChild(tile);

  const tiles = document.querySelectorAll(".tile");

// get the maximum height of all the tiles
const maxHeight = Math.max(
  ...Array.from(tiles).map((tile) => tile.offsetHeight)
);

// set the height of all the tiles to be the same as the maximum height
tiles.forEach((tile) => {
  tile.style.height = `${maxHeight}px`;
});
});
});


const messageForm = document.getElementById('MessageForm');
messageForm.addEventListener("submit", async (e) => {

  e.preventDefault();
  let form = e.currentTarget;
  let url = form.action;

  try {
    let formData = new FormData(form);
    let responseData = await postFormFieldsAsJson({ url, formData });
    let { serverDataResponse } = responseData;
    console.log(serverDataResponse);
    alert("Message Sent!")
  } catch (error) {
    console.error(error);
  }
});

async function postFormFieldsAsJson({ url, formData }) {
  let formDataObject = Object.fromEntries(formData.entries());
  let formDataJsonString = JSON.stringify(formDataObject);
  let fetchOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: formDataJsonString,
  };
  let res = await fetch(url, fetchOptions);

  if (!res.ok) {
    let error = await res.text();
    throw new Error(error);
  }
  return res.json();
}