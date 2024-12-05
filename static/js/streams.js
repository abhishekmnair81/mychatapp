// Agora RTC Configuration
const APP_ID = 'beefa750c8a944caae4837eef48352b6';
const TOKEN = sessionStorage.getItem('token');
const CHANNEL = sessionStorage.getItem('room');
let UID = Number(sessionStorage.getItem('UID'));
let NAME = sessionStorage.getItem('name');

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

let localTracks = [];
let remoteUsers = {};

// Join Channel and Display Local Stream
const joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL;

    client.on('user-published', handleUserJoined);
    client.on('user-left', handleUserLeft);

    try {
        UID = await client.join(APP_ID, CHANNEL, TOKEN, UID);

        localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();

        const member = await createMember();

        const player = `
            <div class="video-container" id="user-container-${UID}">
                <div class="video-player" id="user-${UID}"></div>
                <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
            </div>`;
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);

        localTracks[1].play(`user-${UID}`);
        await client.publish(localTracks);
    } catch (error) {
        console.error('Error joining channel or accessing media devices:', error);
        alert('Could not join the room. Returning to the lobby.');
        window.open('/', '_self');
    }
};

// Handle New User Joining
const handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user;
    await client.subscribe(user, mediaType);

    if (mediaType === 'video') {
        const existingPlayer = document.getElementById(`user-container-${user.uid}`);
        if (existingPlayer) existingPlayer.remove();

        const member = await getMember(user);

        const player = `
            <div class="video-container" id="user-container-${user.uid}">
                <div class="video-player" id="user-${user.uid}"></div>
                <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
            </div>`;
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);

        user.videoTrack.play(`user-${user.uid}`);
    }

    if (mediaType === 'audio') user.audioTrack.play();
};

// Handle User Leaving
const handleUserLeft = (user) => {
    delete remoteUsers[user.uid];
    const userContainer = document.getElementById(`user-container-${user.uid}`);
    if (userContainer) userContainer.remove();
};

// Leave and Remove Local Stream
const leaveAndRemoveLocalStream = async () => {
    try {
        localTracks.forEach((track) => {
            track.stop();
            track.close();
        });
        await client.leave();
    } catch (error) {
        console.error('Error leaving the channel:', error);
    }

    await deleteMember();
    window.open('/', '_self');
};

// Toggle Camera
const toggleCamera = async (e) => {
    const isMuted = localTracks[1].muted;
    await localTracks[1].setMuted(!isMuted);
    e.target.style.backgroundColor = isMuted ? '#fff' : 'rgb(255, 80, 80)';
};

// Toggle Microphone
const toggleMic = async (e) => {
    const isMuted = localTracks[0].muted;
    await localTracks[0].setMuted(!isMuted);
    e.target.style.backgroundColor = isMuted ? '#fff' : 'rgb(255, 80, 80)';
};

// Helper Functions
const createMember = async () => {
    try {
        const response = await fetch('/create_member/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: NAME, room_name: CHANNEL, UID }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error creating member:', error);
        return { name: 'Unknown' };
    }
};

const getMember = async (user) => {
    try {
        const response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching member info:', error);
        return { name: 'Unknown' };
    }
};

const deleteMember = async () => {
    try {
        await fetch('/delete_member/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: NAME, room_name: CHANNEL, UID }),
        });
    } catch (error) {
        console.error('Error deleting member:', error);
    }
};

// Event Listeners
window.addEventListener('beforeunload', deleteMember);
joinAndDisplayLocalStream();

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream);
document.getElementById('camera-btn').addEventListener('click', toggleCamera);
document.getElementById('mic-btn').addEventListener('click', toggleMic);
