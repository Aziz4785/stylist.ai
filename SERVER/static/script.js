const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const searchResult = document.getElementById("search-result");
const showMoreBtn = document.getElementById("show-more-btn");
const leftArrowSvg = '<svg>Your left arrow SVG here</svg>';
const rightArrowSvg = '<svg>Your right arrow SVG here</svg>';



searchBox.addEventListener('input', function() {
    // Set the height to 'auto' to get the correct scrollHeight
    this.style.height = 'auto';
    
    // Define a threshold height, for example, the height of one line of text
    var thresholdHeight = 42; // Adjust this value as needed

    // Only adjust the height if the scrollHeight exceeds the threshold
    if (this.scrollHeight > thresholdHeight) {
        this.style.height = this.scrollHeight + 'px';
    } else {
        // If below threshold, set it back to the default fixed height
        this.style.height = thresholdHeight + 'px';
    }
});

function mockApiCall(query) {
    // Retrieve the CSRF token from the hidden input field
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    return fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: 'query=' + encodeURIComponent(query)
    })
    .then(response => {
        // Extract rate limit headers
        const rateLimitInfo = {
            limit: response.headers.get('X-RateLimit-Limit'),
            remaining: response.headers.get('X-RateLimit-Remaining'),
            reset: response.headers.get('X-RateLimit-Reset')
        };

        // Parse the JSON response and pass along rate limit info
        return response.json().then(data => ({ data, rateLimitInfo }));
    });
}

searchForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    document.getElementById('loading-animation').style.display = 'block';
    searchResult.innerHTML = '';
    const query = searchBox.value;
    mockApiCall(query).then(response => {

        const data = response.data;
        const rateLimitInfo = response.rateLimitInfo;

        const rateLimitDisplay = document.getElementById('rate-limit-info'); // Ensure this element exists in your HTML
        rateLimitDisplay.textContent = `${rateLimitInfo.remaining}/${rateLimitInfo.limit} `;

        // Clear previous results
        searchResult.innerHTML = '';

        if (!data || data.length === 0) {
            document.getElementById('loading-animation').style.display = 'none';
            // Optionally, you can display a message indicating no results were found
            searchResult.innerHTML = '<p>No results found.</p>';
            return;
        }
        // Process each item and add to the grid
        data.forEach(item => {

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
                img.style.display = index === 0 ? 'block' : 'none'; // Display only the first image initially
                carousel.appendChild(img);
            });

            const prevButton = document.createElement('button');
            prevButton.innerHTML = '&#10094;'; // Left arrow symbol
            prevButton.className = 'carousel-control prev';

            const nextButton = document.createElement('button');
            nextButton.innerHTML = '&#10095;'; // Right arrow symbol
            nextButton.className = 'carousel-control next';

            // Append buttons to itemContainer
            itemContainer.appendChild(prevButton);
            itemContainer.appendChild(nextButton);

            linkElement.appendChild(carousel); 
            itemContainer.appendChild(linkElement);

            searchResult.appendChild(itemContainer);
            document.getElementById('loading-animation').style.display = 'none';

            // Carousel functionality
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