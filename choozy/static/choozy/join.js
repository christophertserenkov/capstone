/*
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#joinform');

    form.onsubmit = (event) => {
        event.preventDefault()
        const roomId = document.querySelector('#roomid').value;
        const name = document.querySelector('#username').value;

        localStorage.setItem('player', JSON.stringify({'room_id': roomId, 'name': name}));
        form.submit()
    };
});
*/