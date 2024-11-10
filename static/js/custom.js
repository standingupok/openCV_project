const resultDisplay = document.getElementById("result_display");
// navigation  menu js
const buttonPredict = document.getElementById("button_predict");
function openNav() {
  $("#myNav").addClass("menu_width");
  $(".menu_btn-style").fadeIn();
}

function closeNav() {
  $("#myNav").removeClass("menu_width");
  $(".menu_btn-style").fadeOut();
}

// get current year

function displayYear() {
  var d = new Date();
  var currentYear = d.getFullYear();
  document.querySelector("#displayYear").innerHTML = currentYear;
}
displayYear();

// owl carousel slider js
$(".team_carousel").owlCarousel({
  loop: true,
  margin: 0,
  dots: true,
  autoplay: true,
  autoplayHoverPause: true,
  center: true,
  responsive: {
    0: {
      items: 1,
    },
    480: {
      items: 2,
    },
    768: {
      items: 3,
    },
    1000: {
      items: 5,
    },
  },
});

buttonPredict.addEventListener("click", async function () {
  const formData = new FormData(document.getElementById("upload-form"));
  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (data.error) {
      alert(data.error);
    } else {
      data.files.forEach((file) => {
        const img_container = document.createElement("div");
        img_container.classList.add("col");
        img_container.innerHTML = `
                <div class="cover-image">
                  <h2>Prediction Result</h2>
                  <img
                    id="uploaded-image"
                    src="${file.image_url}?t=${new Date().getTime()}"
                    alt="Uploaded Image"
                    style="max-width: 300px"
                  />
                </div>`;
        resultDisplay.appendChild(img_container);
      });
    }
  } catch (error) {
    console.error("Error:", error);
  }
});

// async function submitForm() {
//   const formData = new FormData(document.getElementById("upload-form"));

//   try {
//     const response = await fetch("/predict", {
//       method: "POST",
//       body: formData,
//     });
//     const data = await response.json();

//     if (data.error) {
//       alert(data.error);
//     } else {
//       const img_container = `<div id="result">
//               <h2>Prediction Result</h2>
//               <p id="emotion">${data.image_url}</p>
//               <img
//                 id="uploaded-image"
//                 src="${data.image_url}"
//                 alt="Uploaded Image"
//                 style="display: none; max-width: 300px"
//               />`;
//       resultDisplay.appendChild();
//     }
//   } catch (error) {
//     console.error("Error:", error);
//   }
// }
