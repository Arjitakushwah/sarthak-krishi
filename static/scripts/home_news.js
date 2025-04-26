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

    const url = `https://newsapi.org/v2/everything?q=farming india&from=${fromDate}&to=${toDate}&sortBy=publishedAt&language=en&apiKey=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const articles = data.articles;
            const carousel = document.getElementById('carouselItems');

            if (articles.length === 0) {
                carousel.innerHTML = '<p class="text-center">No news available.</p>';
            } else {
                articles.slice(0, 9).forEach((article) => { // show 9 news initially
                    const item = document.createElement('div');
                    item.className = 'swiper-slide';  // Important for swiper
                    item.innerHTML = `
                        <div class="card h-100 shadow">
                            <img src="${article.urlToImage ? article.urlToImage : 'path/to/placeholder.jpg'}" class="card-img-top" style="height:200px; object-fit:cover;" alt="...">
                            <div class="card-body">
                                <h6 class="card-title">${article.title}</h6>
                                <a href="${article.url}" target="_blank" class="btn btn-outline-primary btn-sm mt-2">Read More</a>
                            </div>
                        </div>
                    `;
                    carousel.appendChild(item);
                });

                // Initialize Swiper after loading news
                new Swiper('.mySwiper', {
                    slidesPerView: 3,   // Show 3 cards at a time
                    spaceBetween: 30,   // Space between slides
                    loop: true,         // Loop infinite
                    autoplay: {
                        delay: 2500,     // Auto scroll every 2.5 seconds
                        disableOnInteraction: false,
                    },
                    breakpoints: {
                        // Responsive
                        320: { slidesPerView: 1 },
                        768: { slidesPerView: 2 },
                        1024: { slidesPerView: 3 },
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error fetching news:', error);
        });
});
