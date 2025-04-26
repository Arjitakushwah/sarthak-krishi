document.addEventListener('DOMContentLoaded', function() {
    const apiKey = 'e07b579ac1e14c24988e583b5864f621';
    const today = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(today.getDate() - 7);

    const formatDate = (date) => {
        return date.toISOString().split('T')[0];
    };

    const fromDate = formatDate(sevenDaysAgo);
    const toDate = formatDate(today);

    const url = `https://newsapi.org/v2/everything?q=farming organic farming india&from=${fromDate}&to=${toDate}&sortBy=publishedAt&language=en&apiKey=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const articles = data.articles;
            const newsContainer = document.getElementById('newsContainer');

            if (articles.length === 0) {
                newsContainer.innerHTML = '<p>No news available right now.</p>';
            } else {
                articles.forEach(article => {
                    const articleCard = document.createElement('div');
                    articleCard.classList.add('col-md-4', 'mb-4');

                    articleCard.innerHTML = `
                        <div class="card shadow-sm h-100">
                            <img src="${article.urlToImage ? article.urlToImage : 'path/to/placeholder.jpg'}" class="card-img-top" alt="Article Image">
                            <div class="card-body">
                                <h5 class="card-title">${article.title}</h5>
                                <p class="card-text">${article.description ? article.description : ''}</p>
                                <p class="text-muted small">Published: ${new Date(article.publishedAt).toLocaleDateString()}</p>
                                <a href="${article.url}" target="_blank" class="btn btn-primary">Read More</a>
                            </div>
                        </div>
                    `;

                    newsContainer.appendChild(articleCard);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching news:', error);
        });
});
