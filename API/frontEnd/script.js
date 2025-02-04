// Function to fetch and display messages
async function fetchMessages() {
    try {
        const response = await fetch('http://127.0.0.1:8000/messages');
        const data = await response.json();
        const content = document.getElementById('content');
        content.innerHTML = '';  // Clear existing content

        data.forEach(message => {
            const messageCard = document.createElement('div');
            messageCard.classList.add('message-card');

            messageCard.innerHTML = `
                <h3>${message.channel_title}</h3>
                <p><span>Username:</span> ${message.channel_username}</p>
                <p><span>Message ID:</span> ${message.message_id}</p>
                <p><span>Message:</span> ${message.message}</p>
                <p><span>Date:</span> ${new Date(message.message_date).toLocaleString()}</p>
                <p><span>Media Path:</span> ${message.media_path}</p>
                <p><span>Emoji Used:</span> ${message.emoji_used}</p>
                <p><span>YouTube Links:</span> ${message.youtube_links}</p>
                <button class="btn-edit" data-id="${message.id}">Edit</button>
                <button class="btn-delete" data-id="${message.id}">Delete</button>
            `;

            content.appendChild(messageCard);
        });

        // Add event listeners for edit and delete buttons
        document.querySelectorAll('.btn-edit').forEach(button => {
            button.addEventListener('click', editMessage);
        });
        document.querySelectorAll('.btn-delete').forEach(button => {
            button.addEventListener('click', deleteMessage);
        });
    } catch (error) {
        console.error('Error fetching messages:', error);
        document.getElementById('content').innerText = 'Error fetching messages. See console for details.';
    }
}

// Function to create a new message
async function createMessage(event) {
    event.preventDefault();
    const form = document.getElementById('create-message-form');
    const message = {
        channel_title: form.channel_title.value,
        channel_username: form.channel_username.value,
        message_id: parseInt(form.message_id.value),
        message: form.message.value,
        message_date: new Date(form.message_date.value).toISOString(),
        media_path: form.media_path.value,
        emoji_used: form.emoji_used.value,
        youtube_links: form.youtube_links.value
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/messages/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(message)
        });
        const data = await response.json();
        console.log('Message created:', data);
        document.getElementById('success-message').style.display = 'block';
        setTimeout(() => {
            document.getElementById('success-message').style.display = 'none';
        }, 3000);
        form.reset();  // Clear form fields
        fetchMessages();
    } catch (error) {
        console.error('Error creating message:', error);
    }
}

// Function to edit an existing message
async function editMessage(event) {
    const id = event.target.getAttribute('data-id');
    const messageCard = event.target.closest('.message-card');
    const form = document.getElementById('create-message-form');

    // Populate the form with existing message details for editing
    form.channel_title.value = messageCard.querySelector('h3').innerText;
    form.channel_username.value = messageCard.querySelector('p:nth-child(2)').innerText.split(": ")[1];
    form.message_id.value = parseInt(messageCard.querySelector('p:nth-child(3)').innerText.split(": ")[1]);
    form.message.value = messageCard.querySelector('p:nth-child(4)').innerText.split(": ")[1];
    form.message_date.value = new Date(messageCard.querySelector('p:nth-child(5)').innerText.split(": ")[1]).toISOString().slice(0, -1);
    form.media_path.value = messageCard.querySelector('p:nth-child(6)').innerText.split(": ")[1];
    form.emoji_used.value = messageCard.querySelector('p:nth-child(7)').innerText.split(": ")[1];
    form.youtube_links.value = messageCard.querySelector('p:nth-child(8)').innerText.split(": ")[1];

    // Submit the form to update the message
    form.onsubmit = async function(event) {
        event.preventDefault();
        const updatedMessage = {
            channel_title: form.channel_title.value,
            channel_username: form.channel_username.value,
            message_id: parseInt(form.message_id.value),
            message: form.message.value,
            message_date: new Date(form.message_date.value).toISOString(),
            media_path: form.media_path.value,
            emoji_used: form.emoji_used.value,
            youtube_links: form.youtube_links.value
        };

        try {
            const response = await fetch(`http://127.0.0.1:8000/messages/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedMessage)
            });
            const data = await response.json();
            console.log('Message updated:', data);
            form.reset();  // Clear form fields
            fetchMessages();
        } catch (error) {
            console.error('Error updating message:', error);
        }
    };
}

// Function to delete a message
async function deleteMessage(event) {
    const id = event.target.getAttribute('data-id');

    try {
        const response = await fetch(`http://127.0.0.1:8000/messages/${id}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            console.log('Message deleted');
            fetchMessages();
        } else {
            console.error('Error deleting message');
        }
    } catch (error) {
        console.error('Error deleting message:', error);
    }
}

// Function to toggle the display of existing messages
function toggleMessages() {
    const content = document.getElementById('content');
    const toggleButton = document.getElementById('toggle-messages');

    if (content.style.display === 'none') {
        content.style.display = 'block';
        toggleButton.innerText = 'Hide Existing Telegram Messages';
        fetchMessages();
    } else {
        content.style.display = 'none';
        toggleButton.innerText = 'Show Existing Telegram Messages';
    }
}

// Event listeners
document.getElementById('create-message-form').addEventListener('submit', createMessage);
document.getElementById('toggle-messages').addEventListener('click', toggleMessages);
window.onload = () => {
    document.getElementById('content').style.display = 'none';
};
