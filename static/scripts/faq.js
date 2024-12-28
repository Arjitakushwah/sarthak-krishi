document.addEventListener('DOMContentLoaded', () => {
    const faqContainer = document.getElementById('faq-container');
    const searchInput = document.getElementById('search-input');

    // Fetch FAQs from JSON
    fetch('/api/faqs')
        .then(response => response.json())
        .then(data => renderFAQs(data));

    // Render FAQs
    function renderFAQs(faqs) {
        faqContainer.innerHTML = '';
        faqs.forEach(faq => {
            const faqElement = document.createElement('div');
            faqElement.classList.add('faq-item');
            faqElement.innerHTML = `
                <h3>${faq.question}</h3>
                <p>${faq.answer}</p>
            `;
            faqContainer.appendChild(faqElement);
        });
    }

    // Search FAQs
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        fetch('/api/faqs')
            .then(response => response.json())
            .then(data => {
                const filteredFAQs = data.filter(faq =>
                    faq.question.toLowerCase().includes(query) ||
                    faq.answer.toLowerCase().includes(query)
                );
                renderFAQs(filteredFAQs);
            });
    });
});
