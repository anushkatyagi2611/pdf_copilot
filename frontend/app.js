// let pdfDoc = null;
// let currentPage = 1;
// let pdfId = null;

// const canvas = document.getElementById("pdf-canvas");
// const ctx = canvas.getContext("2d");

// // Load PDF using pdf.js
// document.getElementById("pdf-upload").addEventListener("change", async (e) => {
//   const file = e.target.files[0];
//   if (!file) return;

//   const formData = new FormData();
//   formData.append("file", file);

//   const res = await fetch("http://127.0.0.1:8000/upload_pdf/", {
//     method: "POST",
//     body: formData
//   });

//   const data = await res.json();
//   pdfId = data.pdf_id;

//   const fileReader = new FileReader();
//   fileReader.onload = async function () {
//     const typedarray = new Uint8Array(this.result);

//     pdfDoc = await pdfjsLib.getDocument({ data: typedarray }).promise;
//     renderPage(1);
//   };
//   fileReader.readAsArrayBuffer(file);
// });

// async function renderPage(num) {
//   currentPage = num;
//   document.getElementById("page-num").innerText = `Page: ${num}`;

//   const page = await pdfDoc.getPage(num);
//   const viewport = page.getViewport({ scale: 1.5 });
//   canvas.height = viewport.height;
//   canvas.width = viewport.width;

//   await page.render({ canvasContext: ctx, viewport }).promise;
// }

// // Scroll detection to update current page (optional enhancement)

// // Ask question
// document.getElementById("ask-btn").addEventListener("click", async () => {
//   const question = document.getElementById("question-input").value;
//   if (!question || !pdfId) return;

//   const formData = new FormData();
//   formData.append("pdf_id", pdfId);
//   formData.append("page_num", currentPage - 1); // zero-based
//   formData.append("question", question);

//   const res = await fetch("http://127.0.0.1:8000/ask/", {
//     method: "POST",
//     body: formData
//   });

//   const data = await res.json();

//   const chatBox = document.getElementById("chat-box");
//   chatBox.innerHTML += `<div><strong>You:</strong> ${question}</div>`;
//   chatBox.innerHTML += `<div><strong>AI:</strong> ${data.answer}</div>`;
//   chatBox.scrollTop = chatBox.scrollHeight;

//   document.getElementById("question-input").value = "";
// });
let pdfDoc = null;
let pdfId = null;
let currentPage = 1;

const pdfContainer = document.createElement("div");
pdfContainer.id = "pdf-container";
pdfContainer.style.overflowY = "scroll";
pdfContainer.style.height = "600px"; // Adjust height as needed
document.querySelector(".left-panel").appendChild(pdfContainer);

// Upload and render PDF
document.getElementById("pdf-upload").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://127.0.0.1:8000/upload_pdf/", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  pdfId = data.pdf_id;

  const fileReader = new FileReader();
  fileReader.onload = async function () {
    const typedarray = new Uint8Array(this.result);

    pdfDoc = await pdfjsLib.getDocument({ data: typedarray }).promise;

    // Clear old pages
    pdfContainer.innerHTML = "";

    for (let i = 1; i <= pdfDoc.numPages; i++) {
      await renderPage(i);
    }
  };
  fileReader.readAsArrayBuffer(file);
});

async function renderPage(num) {
  const page = await pdfDoc.getPage(num);
  const viewport = page.getViewport({ scale: 1.5 });

  const canvas = document.createElement("canvas");
  canvas.classList.add("pdf-page-canvas");
  canvas.dataset.pageNumber = num;

  canvas.height = viewport.height;
  canvas.width = viewport.width;

  await page.render({ canvasContext: canvas.getContext("2d"), viewport }).promise;

  const pageWrapper = document.createElement("div");
  pageWrapper.style.marginBottom = "20px";
  pageWrapper.appendChild(canvas);

  pdfContainer.appendChild(pageWrapper);
}

// Detect current visible page (basic version)
pdfContainer.addEventListener("scroll", () => {
  const canvases = document.querySelectorAll(".pdf-page-canvas");
  let closest = null;
  let minOffset = Infinity;

  canvases.forEach((canvas) => {
    const rect = canvas.getBoundingClientRect();
    const offset = Math.abs(rect.top - pdfContainer.getBoundingClientRect().top);
    if (offset < minOffset) {
      minOffset = offset;
      closest = canvas;
    }
  });

  if (closest) {
    currentPage = parseInt(closest.dataset.pageNumber);
    document.getElementById("page-num").innerText = `Page: ${currentPage}`;
  }
});

// Ask AI about visible page
document.getElementById("ask-btn").addEventListener("click", async () => {
  const question = document.getElementById("question-input").value;
  if (!question || !pdfId) return;

  const formData = new FormData();
  formData.append("pdf_id", pdfId);
  formData.append("page_num", currentPage - 1); // zero-based
  formData.append("question", question);

  const res = await fetch("http://127.0.0.1:8000/ask/", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div><strong>You:</strong> ${question}</div>`;
  chatBox.innerHTML += `<div><strong>AI:</strong> ${data.answer}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;

  document.getElementById("question-input").value = "";
});
