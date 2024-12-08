document.addEventListener('DOMContentLoaded', (event) => {

    // Copy link to clipboard if the copy button is pressed
    document.querySelector('#copy').onclick = () => {
        navigator.clipboard.writeText(document.querySelector('#link').innerHTML);
        
        const copyAlert = document.querySelector('#copied');
        copyAlert.style.display = 'flex';

        setTimeout(function() {
            copyAlert.style.display = 'none'
        }, 2000);
    };

    // If the user is browsing on a phone than they can swipe to see different 'pages'
    if (window.innerWidth <= 768) {
        // Get 'pages' and the page selectors
        const shareContent = document.querySelector('#shareContent');
        const startContent = document.querySelector('#startContent');
        const selectShare = document.querySelector('#selectShare');
        const selectStart = document.querySelector('#selectStart');

        // Hide amd show the appropriate pages
        shareContent.style.display = 'flex';
        startContent.style.display = 'none';
        selectShare.checked = true;

        // Add event listerners to the page selectors
        selectShare.addEventListener('change', displayShare);
        selectStart.addEventListener('change', displayStart);

        // Swipe detector by CS50 AI
        let startX;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });

        document.addEventListener('touchend', (e) => {
            const endX = e.changedTouches[0].clientX;
            const diffX = endX - startX;
        
            if (diffX > 50) {
                displayShare()
                selectShare.checked = true;
                selectStart.checked = false;
            } else if (diffX < -50) {
                displayStart()
                selectShare.checked = false;
                selectStart.checked = true;
            }
        });

    } else {
        // Hide the page selectors if the user is on a larger device
        document.querySelector('#markers').style.display = 'none';
    }

    // Get the player data
    const playerCount = document.querySelector('#playercount');
    const doneCount = document.querySelector('#donecount');
    const userTableBody = document.querySelector('#userTableBody')

    // - setInterval part by CS50AI
    setInterval(() => {

        // Render list of players
        getPlayers().then(data => {
            playerlist = data.players;
            donelist = playerlist.filter(player => player.status === true);

            // Display how namy players are done and how many in total there are
            playerCount.innerHTML = `${playerlist.length}`;
            doneCount.innerHTML = `${donelist.length}/${playerlist.length}`;

            userTableBody.innerHTML = ''

            // Create a table displaying all the players with their names and statuses
            playerlist.forEach(player => {
                const row = document.createElement('tr');
                const name = document.createElement('td');
                const status = document.createElement('td');
                status.className = 'flex justify-center';

                name.innerHTML = `${player.username}`
                if (player.status) {
                    status.innerHTML = '<img class="w-4" src="https://cdn-icons-png.freepik.com/512/5610/5610944.png" alt="check">';
                } else {
                    status.innerHTML ='<img class="w-4" src="https://cdn-icons-png.flaticon.com/512/11450/11450177.png" alt="check">';
                }

                row.append(name, status);
                userTableBody.appendChild(row);
            });

        });
    }, 3000);
});

// Function to display the share page
function displayShare() {
    shareContent.style.display = 'flex';
    startContent.style.display = 'none';
}

// Function to display the player list
function displayStart() {
    shareContent.style.display = 'none';
    startContent.style.display = 'flex';
}

// Function that makes an API call to get player data
function getPlayers() {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const roomId = document.querySelector('meta[name="room_id"]').getAttribute('content');

    // Return API response
    return fetch(`/api/room/${roomId}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json());
}