const resultDisplay = document.getElementById("result_display");
const buttonPredict = document.getElementById("button-predict");
const buttonPredictCamera = document.getElementById("button-predict__camera");
const uploadButton = document.querySelector(".upload-button");
const uploadForm = document.getElementById("upload-form");
const imgContainer = document.querySelector(".img-container");
const text = document.querySelector(".innet");
const browse = document.querySelector(".select");
const formInput = document.querySelector(".form-input.file");
const textProcessing = document.getElementById("text-processing");

// load images
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
  files.forEach((file, index) => {
    const fileType = file.type;
    if (fileType.startsWith("image/")) {
      // Hiển thị ảnh
      images += `<div class="image">
                    <img src="${URL.createObjectURL(file)}" alt="" />
                    <span onclick="delImage(${index})">&times;</span>
                  </div>`;
    } else if (fileType.startsWith("video/")) {
      // Hiển thị video
      images += `<div class="image">
                    <video controls>
                      <source src="${URL.createObjectURL(
                        file
                      )}" type="${fileType}">
                      Your browser does not support the video tag.
                    </video>
                    <span onclick="delImage(${index})">&times;</span>
                  </div>`;
    }
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
  textProcessing.classList.remove("hidden-text");

  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });

  try {
    files = [];
    showImages();
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    textProcessing.classList.add("hidden-text");

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
      });
    }
  } catch (error) {
    console.error("Error:", error);
  }
});

buttonPredictCamera.addEventListener("click", async function () {
  try {
    const response = await fetch("/predict_camera", { method: "GET" });
    const data = await response.json();
    if (data.error) alert(data.error);
    else alert("Camera processing completed.");
  } catch (error) {
    console.log("Error: ", error);
    alert("An error occured while processing the camera input.");
  }
});
