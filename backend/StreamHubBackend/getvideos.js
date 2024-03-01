const { createClient } = require('pexels');
const { exec } = require('child_process');
const { v4: uuidv4 } = require('uuid'); // Import the uuid library for generating unique filenames

const client = createClient('7qJkVW5HifcFeRZO99b6sA1GpLCvzLjMs61TCYVXznukWCpOlTxyTPNp');

client.videos.popular({ per_page: 2 })
    .then(data => {
        const videos = data.videos; // Access the 'videos' property
        videos.forEach(video => {
            const hdVideo = video.video_files.find(file => file.quality === 'hd');
            if (hdVideo && video.duration < 20) {
                console.log(video);
                console.log(hdVideo);
                const videoUrl = hdVideo.link;
                const randomFileName = generateRandomFileName();
                downloadWithIDM(videoUrl, randomFileName);
                console.log(`Video downloaded with filename: ${randomFileName}`);
            }
        });
    })
    .catch(error => {
        console.error('Error fetching videos:', error);
    });

function downloadWithIDM(url, fileName) {
    // Replace 'idman.exe' with the actual path to IDM executable on your machine
    const idmPath = 'C:\\Program Files (x86)\\Internet Download Manager\\idman.exe';

    // Use IDM command-line parameters to initiate download with the specified filename
    const idmCommand = `"${idmPath}" /n /a /d "${url}" /p "C:\\Users\\karan\\OneDrive\\Documents\\GitHub\\StreamHub-backend\\backend\\StreamHubBackend\\media\\user_uploads" /f "${fileName}"`;

    require('child_process').exec(idmCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
        } else {
            console.log(`IDM Output: ${stdout}`);
    
            // Handle actions after IDM process completion here
            console.log('IDM download complete!');
        }
    });
}

function generateRandomFileName() {
    return `${uuidv4()}.mp4`; // Use UUID to generate a unique filename with the .mp4 extension
}
