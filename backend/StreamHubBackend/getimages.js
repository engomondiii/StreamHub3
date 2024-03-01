const { createClient } = require('pexels');
const { exec } = require('child_process');
const { v4: uuidv4 } = require('uuid');

const client = createClient('7qJkVW5HifcFeRZO99b6sA1GpLCvzLjMs61TCYVXznukWCpOlTxyTPNp');

// Set the initial page
let currentPage = 1;

// Define the number of images per page
const imagesPerPage = 2;

// Function to fetch and download images recursively
function fetchAndDownloadImages() {
    client.photos.curated({ page: currentPage, per_page: imagesPerPage })
        .then(data => {
            const photos = data.photos;
            if (photos.length > 0) {
                photos.forEach(photo => {
                    const imageUrl = photo.src.large;
                    const randomFileName = generateRandomFileName('jpg');
                    downloadWithIDM(imageUrl, randomFileName);
                    console.log(`Image downloaded with filename: ${randomFileName}`);
                });

                // Move to the next page
                currentPage++;

                // Recursively call the function for the next page
                fetchAndDownloadImages();
            } else {
                // No more pages available
                console.log('No more pages available.');
            }
        })
        .catch(error => {
            console.error('Error fetching images:', error);
        });
}

// Start fetching and downloading images
fetchAndDownloadImages();

function downloadWithIDM(url, fileName) {
    const idmPath = 'C:\\Program Files (x86)\\Internet Download Manager\\idman.exe';
    const idmCommand = `"${idmPath}" /n /d "${url}" /p "C:\\Users\\karan\\OneDrive\\Documents\\GitHub\\StreamHub-backend\\backend\\StreamHubBackend\\media\\user_uploads" /f "${fileName}"`;

    require('child_process').exec(idmCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
        } else {
            console.log(`IDM Output: ${stdout}`);
            console.log('IDM download complete!');
        }
    });
}

function generateRandomFileName(extension) {
    return `${uuidv4()}.${extension}`;
}
