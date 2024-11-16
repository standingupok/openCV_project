const resultDisplay = document.getElementById("result_display");
const buttonPredict = document.getElementById("button_predict");
const uploadButton = document.querySelector(".upload-button");
const uploadForm = document.getElementById("upload-form");
const imgContainer = document.querySelector(".img-container");
const text = document.querySelector(".innet");
const browse = document.querySelector(".select");
const formInput = document.querySelector(".form-input.file");
// navigation  menu js
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

// load file
let files = [];
browse.addEventListener("click", () => formInput.click());
formInput.addEventListener("change", () => {
  const file = formInput.files;
  for (let i = 0; i < file.length; i++) {
    if (files.every((e) => e.name != file[i].name)) files.push(file[i]);
  }
  uploadForm.reset();
  showImages();
});

const showImages = () => {
  let images = "";
  files.forEach((e, i) => {
    images += `<div class="image">
                <img src="${URL.createObjectURL(e)}" alt="" />
                <span onclick="delImage(${i})">&times;</span
                >
              </div>`;
  });

  imgContainer.innerHTML = images;
};

const delImage = (index) => {
  files.splice(index, 1);
  showImages();
};

uploadForm.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadForm.classList.add("drag-hover");
  text.innerHTML = `Drop images`;
});

uploadForm.addEventListener("dragleave", (e) => {
  e.preventDefault();
  uploadForm.classList.remove("drag-hover");
  text.innerHTML = `Drag & drop image here or <span class="select">Browse</span>`;
});

uploadForm.addEventListener("drop", (e) => {
  e.preventDefault();

  uploadForm.classList.remove("drag-hover");
  text.innerHTML = `Drag & drop image here or <span class="select">Browse</span>`;

  const file = e.dataTransfer.files;
  for (let i = 0; i < file.length; i++) {
    if (files.every((e) => e.name != file[i].name)) files.push(file[i]);
  }
  showImages();
});

uploadButton.addEventListener("click", () => formInput.click());

// predict
buttonPredict.addEventListener("click", async function () {
  // const formData = new FormData(uploadForm);
  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });

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
        img_container.classList.add("gallery-img-box");
        if (file.isImage) {
          img_container.innerHTML = `
          <img
          id="uploaded-image"
          src="${file.image_url}?t=${new Date().getTime()}"
          alt="Uploaded Image"
          style="max-width:100%"
          />`;
        } else {
          img_container.innerHTML = `<video
          id="uploaded-video"
          controls
          style="max-width:100%"
          >
          <source src="${file.image_url}" type="video/mp4">
          Your browser does not support the video tag.
          </video>`;
        }
        resultDisplay.insertBefore(img_container, resultDisplay.firstChild);
        files = [];
        showImages();
      });
    }
  } catch (error) {
    console.error("Error:", error);
  }
});
