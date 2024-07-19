class SocketService {
  socket;

  connect() {
    const token = localStorage.getItem("access");
    const wsUrl = `${process.env.REACT_APP_WS_HOST}/ws/chat/?token=${token}`
    this.socket = new WebSocket(wsUrl);  // Replace with your Django server URL

    this.socket.onopen = () => {
      console.log('Connected to server');
    };

    this.socket.onclose = () => {
      console.log('Disconnected from server');
    };
  }

  sendMessage(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    }
  }

  onMessage(callback) {
    if (this.socket) {
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        callback(data);
      };
    }
  }
}

const socketService = new SocketService();
export default socketService;
