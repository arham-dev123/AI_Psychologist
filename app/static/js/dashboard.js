const fallbackArticles = [
  {
    containerId: 'card1',
    url: 'https://mexicobariatriccenter.com/grounding-exercises-for-anxiety/',
    title: 'Grounding Exercises for Anxiety',
    imageUrl: '/static/img/card1.png'
  },
  {
    containerId: 'card2',
    url: 'https://www.helpguide.org/articles/anxiety/anxiety-medication.htm',
    title: 'Anxiety Medication: What You Need to Know',
    imageUrl: '/static/img/card3.png'
  }
];

function createArticleCard(article) {
  return `
    <a href="${article.url}" class="btn text-start" target="_blank" rel="noopener noreferrer">
      <div class="card-body">
        <div class="d-flex align-items-center justify-content-left">
          <div class="blog-status-dot"></div>
          <p class="text-muted mb-0 mx-1">DAILY BLOG</p>
        </div>
        <h5 class="card-title text-black py-1">${article.title}</h5>
      </div>
      <img src="${article.imageUrl}" class="card-img-top mw-100 h-72" alt="${article.title}">
    </a>
  `;
}

function renderArticle(article) {
  const container = document.getElementById(article.containerId);

  if (container) {
    container.innerHTML = createArticleCard(article);
  }
}

fallbackArticles.forEach(renderArticle);

Promise.all([
  fetch('https://corsproxy.io/?https://mexicobariatriccenter.com/grounding-exercises-for-anxiety/').then(response => response.text()),
  fetch('https://corsproxy.io/?https://www.helpguide.org/articles/anxiety/anxiety-medication.htm').then(response => response.text())
])
.then(([html1, html2]) => {
  const parser = new DOMParser();
  const doc1 = parser.parseFromString(html1, 'text/html');
  const doc2 = parser.parseFromString(html2, 'text/html');

  const title1 = doc1.querySelector('article[id="post-14006"] h1.entry-title')?.textContent?.trim();
  const imageUrl1 = doc1.querySelector('article[id="post-14006"] img[fetchpriority="high"]')?.getAttribute('src');
  const title2 = doc2.querySelector('h1.post-title')?.textContent?.trim();
  const imageUrl2 = doc2.querySelector('figure.image-wrapper.image-wrapper img.image')?.getAttribute('src');

  renderArticle({
    ...fallbackArticles[0],
    title: title1 || fallbackArticles[0].title,
    imageUrl: imageUrl1 || fallbackArticles[0].imageUrl
  });

  renderArticle({
    ...fallbackArticles[1],
    title: title2 || fallbackArticles[1].title,
    imageUrl: imageUrl2 || fallbackArticles[1].imageUrl
  });
})
.catch(error => {
  console.error('Error fetching webpages:', error);
});
