// Fetch the webpage and extract title and image
Promise.all([
  fetch('https://corsproxy.io/?https://mexicobariatriccenter.com/grounding-exercises-for-anxiety/').then(response => response.text()),
  fetch('https://corsproxy.io/?https://www.helpguide.org/articles/anxiety/anxiety-medication.htm').then(response => response.text())
])
.then(([html1, html2]) => {
    const parser = new DOMParser();

    // Process HTML from the first URL
    const doc1 = parser.parseFromString(html1, 'text/html');
    const title1 = doc1.querySelector('article[id="post-14006"] h1.entry-title').textContent;
    const imageUrl1 = doc1.querySelector('article[id="post-14006"] img[fetchpriority="high"]').getAttribute('src');

    // Create card HTML for the first URL
    const cardHtml1 = `
      <a href="https://mexicobariatriccenter.com/grounding-exercises-for-anxiety/" class="btn text-start">
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-left">
            <div style="width: 10px; height: 10px; background-color: green; border-radius: 50%; margin-right: 5px;"></div>
            <p class="text-muted mb-0 mx-1">DAILY BLOG</p>
          </div>
          <h5 class="card-title text-black py-1">${title1}</h5>
        </div>
        <img src="${imageUrl1}" class="card-img-top mw-100 h-75" alt="Card 1 Image">
      </a>
    `;

    // Process HTML from the second URL
    const doc2 = parser.parseFromString(html2, 'text/html');
    const title2 = doc2.querySelector('h1.post-title').textContent; // Modify this to get the title from the second URL
    const imageUrl2 = doc2.querySelector(' figure.image-wrapper.image-wrapper img.image').getAttribute('src'); // Modify this to get the image URL from the second URL

    // Create card HTML for the second URL
    const cardHtml2 = `
      <a href="https://www.helpguide.org/articles/anxiety/anxiety-medication.htm" class="btn text-start">
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-left">
            <div style="width: 10px; height: 10px; background-color: green; border-radius: 50%; margin-right: 5px;"></div>
            <p class="text-muted mb-0 mx-1">DAILY BLOG</p>
          </div>
          <h5 class="card-title text-black py-1">${title2}</h5>
        </div>
        <img src="${imageUrl2}" class="card-img-top mw-100 h-75" alt="Card 2 Image">
      </a>
    `;

    // Insert card HTML into respective containers
    document.getElementById('card1').innerHTML = cardHtml1;
    document.getElementById('card2').innerHTML = cardHtml2;
})
.catch(error => {
    console.error('Error fetching webpages:', error);
});