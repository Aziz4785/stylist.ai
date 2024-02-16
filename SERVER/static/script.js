const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const searchResult = document.getElementById("search-result");
const showMoreBtn = document.getElementById("show-more-btn");
const leftArrowSvg = '<svg>Your left arrow SVG here</svg>';
const rightArrowSvg = '<svg>Your right arrow SVG here</svg>';

searchBox.addEventListener('input', function() {
    this.style.height = 'auto';
    let thresholdHeight = 42; // Adjust based on your design

    if (this.scrollHeight > thresholdHeight) {
        this.style.height = `${this.scrollHeight}px`;
    } else {
        this.style.height = `${thresholdHeight}px`;
    }
});

function mockApiCall(query) {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    return fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `query=${encodeURIComponent(query)}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json().then(data => {
            const rateLimitInfo = {
                limit: response.headers.get('X-RateLimit-Limit'),
                remaining: response.headers.get('X-RateLimit-Remaining'),
                reset: response.headers.get('X-RateLimit-Reset')
            };
            return { data, rateLimitInfo };
        });
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}

searchForm.addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('loading-animation').style.display = 'block';
    searchResult.innerHTML = '';
    const query = searchBox.value;
    mockApiCall(query).then(response => {
        document.getElementById('loading-animation').style.display = 'none';

        if (!response || !response.data || !Array.isArray(response.data.result)) {
            console.error('No response from the API or data is not in the expected format:', response);
            searchResult.innerHTML = '<p>No results found or data is not in expected format.</p>';
            return;
        }
        const items = response.data.result;
        const searchesLeft = response.data.searches_left;
        
        const rateLimitDisplay = document.getElementById('rate-limit-info');
        rateLimitDisplay.textContent = `${searchesLeft}/100`;

        items.forEach(item => {
            const itemContainer = document.createElement('div');
            itemContainer.className = 'item-container';
            const linkElement = document.createElement('a');
            linkElement.href = item.url;
            linkElement.target = '_blank';

            const carousel = document.createElement('div');
            carousel.className = 'carousel';

            item.images.forEach((imageSrc, index) => {
                const img = document.createElement('img');
                img.src = imageSrc;
                img.className = 'carousel-image';
                img.style.display = index === 0 ? 'block' : 'none';
                carousel.appendChild(img);
            });

            const prevButton = document.createElement('button');
            prevButton.innerHTML = leftArrowSvg;
            prevButton.className = 'carousel-control prev';

            const nextButton = document.createElement('button');
            nextButton.innerHTML = rightArrowSvg;
            nextButton.className = 'carousel-control next';

            linkElement.appendChild(carousel);
            itemContainer.appendChild(linkElement);
            itemContainer.appendChild(prevButton);
            itemContainer.appendChild(nextButton);
            searchResult.appendChild(itemContainer);

            let currentImageIndex = 0;
            const images = carousel.querySelectorAll('.carousel-image');

            prevButton.addEventListener('click', () => {
                images[currentImageIndex].style.display = 'none';
                currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
                images[currentImageIndex].style.display = 'block';
            });

            nextButton.addEventListener('click', () => {
                images[currentImageIndex].style.display = 'none';
                currentImageIndex = (currentImageIndex + 1) % images.length;
                images[currentImageIndex].style.display = 'block';
            });
        });
    });
});