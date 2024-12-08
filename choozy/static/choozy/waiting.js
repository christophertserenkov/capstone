document.addEventListener('DOMContentLoaded', () => {
    const playercount = document.querySelector('#playercount');
    const playersDone = document.querySelector('#playersDone');
    const loading = document.querySelector('#loading');

    // Hide player count and display loading indicator
    playercount.style.display = 'none';
    loading.style.display = 'block';

    // Update playercount every 5 seconds
    setInterval(() => {
        // Get the CSRF token and room id
        const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const roomId = document.querySelector('meta[name="room_id"]').getAttribute('content');

        // Make an API request and display done players and all players
        fetch(`/api/room/${roomId}/players`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Reload page to view results if the room is closed
            if (data.room_status === false) {
                location.reload()
            } else {
                // Render the player count
                playersDone.innerHTML = `${data.players_done}/${data.players}`;

                // Show the playercount and hide the loading indicator
                loading.style.display = 'none';
                playercount.style.display = 'flex';
            }
        })
        .catch(error => {
            console.log(error)
        });
    }, 5000)
});
