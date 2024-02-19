const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const searchResult = document.getElementById("search-result");
const showMoreBtn = document.getElementById("show-more-btn");
const loadingMessages = [
    "Let me check my inventory...",
    "Give me a moment to find your fashion match...",
    "Filtering through my vast selection just for you...",
    "Finding the perfect fit...",
    "Almost there, just verifying to ensure nothing was missed...",
    "Ensuring your search results are top-notch and tailored to you..."
];

let currentMessageIndex = 0; 

function updateLoadingMessage() {
    if (currentMessageIndex >= loadingMessages.length) {
        currentMessageIndex = 0; 
    }
    const message = loadingMessages[currentMessageIndex++];
    document.getElementById('loading-message').textContent = message;
}

function startLoadingMessages() {
    updateLoadingMessage(); // Display the first message immediately

    // Set an interval to update the message every X seconds
    return setInterval(updateLoadingMessage, 7000); // Returns the interval ID
}


function showLoadingAnimation() {
    const loadingAnimation = document.querySelector('.lds-ripple');
    loadingAnimation.style.display = 'block'; // Show the loading animation

    // Start cycling through the loading messages
    const messageIntervalId = startLoadingMessages();

    // Store the interval ID for later use (to clear the interval)
    loadingAnimation.setAttribute('data-message-interval-id', messageIntervalId);
}

function hideLoadingAnimation() {
    const loadingAnimation = document.querySelector('.lds-ripple');
    loadingAnimation.style.display = 'none'; // Hide the loading animation

    // Hide the loading message
    document.getElementById('loading-message').textContent = '';

    // Clear the interval that updates the loading message
    const messageIntervalId = loadingAnimation.getAttribute('data-message-interval-id');
    clearInterval(messageIntervalId);
}

function extractRateLimitInfo(response) {
    return {
        limit: response.headers.get('X-RateLimit-Limit'),
        remaining: response.headers.get('X-RateLimit-Remaining'),
        reset: response.headers.get('X-RateLimit-Reset')
    };
}

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

function sendQueryToServer(query) {
    console.log("Attempting to fetch data for query:", query);

    const controller = new AbortController();
    const signal = controller.signal;
    const timeoutId = setTimeout(() => controller.abort(), 120000);
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `query=${encodeURIComponent(query)}`,
        signal: signal
    })
    .then(response => handleResponse(response)) // Process the response
    .catch(error => {
        console.error('Error:', error);
        hideLoadingAnimation(); // Hide loading animation on error
    }); // Handle any error that occurred in the fetch operation
}

async function handleResponse(response) {
    hideLoadingAnimation();
    const rateLimitInfo = extractRateLimitInfo(response); // Extract rate limit information
    console.log(rateLimitInfo); // Example of how to use the rate limit information
    displayRateLimitInfo(rateLimitInfo);

    if (!response.ok) {
        handleError(response.status); // Handle HTTP errors
    } else {
        const data = await response.json();
        if (Object.keys(data).length === 0) {
            document.getElementById('searchResult').innerHTML = '<p>no results found</p>';
        } else {
            processData(data); // Process and display the data
        }
    }
}

function displayRateLimitInfo(rateLimitInfo) {
    const rateLimitDisplay = document.getElementById('rate-limit-info');
    if (rateLimitInfo && rateLimitInfo.remaining) {
        rateLimitDisplay.textContent = `${rateLimitInfo.remaining}/${rateLimitInfo.limit}`;
    } else {
        rateLimitDisplay.textContent = '-';
    }
}
function handleError(statusCode) {
    if (statusCode === 400) {
        searchResult.innerHTML = '<p>Invalid input</p>';
    } else if (statusCode === 500) {
        searchResult.innerHTML = '<p>Error, please try again</p>';
    } else {
        searchResult.innerHTML = '<p>An error occurred, please try again later</p>';
    }
}

function processData(data) {
    // This function should be implemented to display the data
    // For example:
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
}

// function mockApiCall(query) {
    

//     // Create an AbortController instance
//     const controller = new AbortController();
//     const signal = controller.signal;

//     // Set a timeout to abort the fetch operation after 120000 milliseconds (2 minutes)
//     const timeoutId = setTimeout(() => controller.abort(), 120000);

//     // Retrieve the CSRF token from the hidden input field
//     const csrfToken = document.querySelector('input[name="csrf_token"]').value;

//      // Correctly encode the body data
//      const encodedBody = `query=${encodeURIComponent(query)}`; // Fixed incorrect body format

//     return fetch('/process', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//             'X-CSRFToken': csrfToken
//         },
//         body: `query=${encodeURIComponent(query)}`,
//         signal: signal
//     })
//     .then(response => {
//         clearTimeout(timeoutId); // Clear the timeout as the fetch completed in time

//         if (!response.ok) {
//             return Promise.reject(new Error('Network response was not ok'));
//         }
//         return response.json().then(data => {
//             console.log("resposne received");
//             if (data && data.error) {
//                 return Promise.reject(new Error('An unexpected error occurred'));
//             }
//             console.log("init rate limit");
//             const rateLimitInfo = {
//                 limit: response.headers.get('X-RateLimit-Limit'),
//                 remaining: response.headers.get('X-RateLimit-Remaining'),
//                 reset: response.headers.get('X-RateLimit-Reset')
//             };
//             return { data: data || {}, rateLimitInfo };
//         });
//     })
//     .catch(error => {
//         clearTimeout(timeoutId); // Ensure the timeout is cleared to avoid memory leaks
//         console.log("error is catched");
//         console.error('Fetch operation error:', error);
        
//         searchResult.innerHTML = '<p>Error please try again</p>';
//         return { error: true, message: error.message };
//     });
// }

searchForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    clearSearchResults(); // Clear previous search results
    const query = searchBox.value;
    showLoadingAnimation(); // Show loading animation
    sendQueryToServer(query);
});
function clearSearchResults() {
    searchResult.innerHTML = '';
}

// searchForm.addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent default form submission
//     searchResult.innerHTML = '';
//     const query = searchBox.value;

//     // Display the loading animation
//     const loadingAnimation = document.querySelector('.lds-ripple');
//     showLoadingAnimation(); // Make sure the loading animation is visible

//     mockApiCall(query).then(response => {
//         hideLoadingAnimation();
//         // Ensure response and its properties are defined before accessing them
//         if(!response || !response.data ){
//             searchResult.innerHTML = '<p>An unexpected error occurred</p>';
//             return;
//         }
//         if (response.data.length === 0) {
//             searchResult.innerHTML = '<p>No results found.</p>';
//             return;
//         }

//         const { data, rateLimitInfo } = response;
        
//         const rateLimitDisplay = document.getElementById('rate-limit-info');
//         if (rateLimitInfo) {
//             rateLimitDisplay.textContent = `${rateLimitInfo.remaining}/${rateLimitInfo.limit}`;
//         } else {
//             // Handle the case where rate limit info might not be available
//             rateLimitDisplay.textContent = 'Rate limit info not available';
//         }

//         // Process each item and add to the grid
//         data.forEach(item => {

//             const itemContainer = document.createElement('div');
//             itemContainer.className = 'item-container';
//             const linkElement = document.createElement('a');
//             linkElement.href = item.url;
//             linkElement.target = '_blank';

//             const carousel = document.createElement('div');
//             carousel.className = 'carousel';

//             item.images.forEach((imageSrc, index) => {
//                 const img = document.createElement('img');
//                 img.src = imageSrc;
//                 img.className = 'carousel-image';
//                 img.style.display = index === 0 ? 'block' : 'none'; // Display only the first image initially
//                 carousel.appendChild(img);
//             });

//             const prevButton = document.createElement('button');
//             prevButton.innerHTML = '&#10094;'; // Left arrow symbol
//             prevButton.className = 'carousel-control prev';

//             const nextButton = document.createElement('button');
//             nextButton.innerHTML = '&#10095;'; // Right arrow symbol
//             nextButton.className = 'carousel-control next';

//             // Append buttons to itemContainer
//             itemContainer.appendChild(prevButton);
//             itemContainer.appendChild(nextButton);

//             linkElement.appendChild(carousel); 
//             itemContainer.appendChild(linkElement);

//             searchResult.appendChild(itemContainer);

//             // Carousel functionality
//             let currentImageIndex = 0;
//             const images = carousel.querySelectorAll('.carousel-image');
            
//             prevButton.addEventListener('click', () => {
//                 images[currentImageIndex].style.display = 'none';
//                 currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
//                 images[currentImageIndex].style.display = 'block';
//             });
            
//             nextButton.addEventListener('click', () => {
//                 images[currentImageIndex].style.display = 'none';
//                 currentImageIndex = (currentImageIndex + 1) % images.length;
//                 images[currentImageIndex].style.display = 'block';
//             });
//         });

//     });
   
// });
