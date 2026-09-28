from datetime import datetime


class IVISimulator:
    def __init__(self):
        self.tracks = [
            "Demo Track 01",
            "Demo Track 02",
            "Demo Track 03",
        ]
        self.track_index = 0
        self.playing = False
        self.volume = 70
        self.logs = []

    def timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def log(self, component, message):
        self.logs.insert(0, {
            "time": self.timestamp(),
            "component": component,
            "message": message,
        })
        self.logs = self.logs[:40]

    def media_service(self, command):
        if command == "play":
            self.playing = True
            self.log("MEDIA SERVICE", "PLAY_REQUEST")
            self.audio_hal("play")
        elif command == "pause":
            self.playing = False
            self.log("MEDIA SERVICE", "PAUSE_REQUEST")
            self.audio_hal("pause")
        elif command == "next":
            self.track_index = (self.track_index + 1) % len(self.tracks)
            self.log("MEDIA SERVICE", "NEXT_TRACK_REQUEST")
            self.audio_hal("play")
            self.playing = True
        elif command == "stop":
            self.playing = False
            self.log("MEDIA SERVICE", "STOP_REQUEST")
            self.audio_hal("stop")

    def audio_hal(self, action):
        if action == "play":
            self.log("AUDIO HAL", "AUDIO_START")
            self.log("AUDIO DRIVER", "OUTPUT_STARTED")
        elif action == "pause":
            self.log("AUDIO HAL", "AUDIO_PAUSE")
            self.log("AUDIO DRIVER", "OUTPUT_PAUSED")
        elif action == "stop":
            self.log("AUDIO HAL", "AUDIO_STOP")
            self.log("AUDIO DRIVER", "OUTPUT_STOPPED")

    def handle_command(self, command):
        self.log("USER INPUT", command.upper())
        self.media_service(command)
        return self.state()

    def set_volume(self, value):
        self.volume = value
        self.log("USER INPUT", f"VOLUME_{value}")
        self.log("MEDIA SERVICE", f"VOLUME_REQUEST: {value}")
        self.log("AUDIO HAL", f"SET_VOLUME: {value}")
        return self.state()

    def state(self):
        return {
            "playing": self.playing,
            "volume": self.volume,
            "track": self.tracks[self.track_index],
            "audio_hal": "ACTIVE" if self.playing else "IDLE",
            "driver": "OUTPUT_ACTIVE" if self.playing else "OUTPUT_IDLE",
            "logs": self.logs,
        }
