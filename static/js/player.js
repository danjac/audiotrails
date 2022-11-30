import Alpine from "alpinejs";

document.addEventListener("alpine:init", () => {
    Alpine.data(
        "player",
        (
            autoplay = false,
            currentTime = 0,
            csrfToken = null,
            timeUpdateUrl = null,
        ) => ({
            autoplay,
            currentTime,
            csrfToken,
            timeUpdateUrl,
            runtime: 0,
            duration: 0,
            isError: false,
            isLoaded: false,
            isPaused: false,
            isPlaying: false,
            timer: null,
            counters: {
                current: "00:00:00",
                total: "00:00:00",
            },
            init() {
                if ("mediaSession" in navigator) {
                    navigator.mediaSession.metadata = this.getMediaMetadata();
                }

                this.$watch("runtime", value => {
                    const percent =
                        value && this.duration
                            ? (value / this.duration) * 100
                            : 0;
                    this.$refs.range.style.setProperty(
                        "--webkitProgressPercent",
                        `${percent}%`,
                    );
                    this.counters.current = this.formatCounter(value);
                });

                this.$watch("duration", value => {
                    this.counters.total = this.formatCounter(value);
                });

                this.$refs.audio.load();
            },
            destroy() {
                this.clearTimer();
            },
            loaded(event) {
                if (this.isLoaded) {
                    return;
                }

                event.target.currentTime = this.currentTime;

                this.isError = false;
                this.duration = event.target.duration || 0;
                this.loadState();

                if (this.autoplay) {
                    event.target.play().catch(this.handleError.bind(this));
                } else {
                    this.pause();
                }

                this.isLoaded = true;
            },
            timeUpdate(event) {
                this.runtime = Math.floor(event.target.currentTime);

                this.isPlaying = true;
                this.isError = false;
            },
            play() {
                this.isPaused = false;
                this.isPlaying = true;
                this.isError = false;
                this.saveState();
                this.startTimer();
            },
            pause() {
                this.isPlaying = false;
                this.isPaused = true;
                this.saveState();
                this.clearTimer();
            },
            ended() {
                this.pause();
                this.runtime = 0;
                this.sendTimeUpdate();
            },
            buffering() {
                this.isPlaying = false;
            },
            error(event) {
                this.handleError(event.target.error);
            },
            togglePlayPause() {
                if (this.isPaused) {
                    this.$refs.audio.play();
                } else {
                    this.$refs.audio.pause();
                }
            },
            skip() {
                if (this.isPlaying) {
                    this.$refs.audio.currentTime = this.runtime;
                }
            },
            skipTo(seconds) {
                if (this.isPlaying) {
                    this.$refs.audio.currentTime += seconds;
                }
            },
            skipBack() {
                this.skipTo(-10);
            },
            skipForward() {
                this.skipTo(10);
            },
            shortcuts(event) {
                if (event.target.tagName.match(/INPUT|TEXTAREA/)) {
                    return;
                }

                const handleEvent = fn => {
                    event.preventDefault();
                    event.stopPropagation();
                    fn.bind(this)();
                };

                if (!event.ctrlKey && !event.altKey) {
                    switch (event.code) {
                        case "Space":
                            return handleEvent(this.togglePlayPause);
                        case "ArrowRight":
                            return handleEvent(this.skipForward);
                        case "ArrowLeft":
                            return handleEvent(this.skipBack);
                    }
                }
            },
            startTimer() {
                if (!this.timer) {
                    this.timer = setInterval(() => {
                        if (this.isPlaying) {
                            this.sendTimeUpdate();
                        }
                    }, 5000);
                }
            },
            clearTimer() {
                if (this.timer) {
                    clearInterval(this.timer);
                    this.timer = null;
                }
            },
            sendTimeUpdate() {
                fetch(this.timeUpdateUrl, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: new URLSearchParams({
                        current_time: this.runtime,
                    }),
                });
            },
            loadState() {
                const state = sessionStorage.getItem("player");
                const { autoplay } = state
                    ? JSON.parse(state)
                    : {
                          autoplay: false,
                      };
                this.autoplay = autoplay || this.autoplay;
            },
            saveState() {
                sessionStorage.setItem(
                    "player",
                    JSON.stringify({
                        autoplay: this.isPlaying,
                    }),
                );
            },
            formatCounter(value) {
                if (isNaN(value) || value < 0) return "00:00:00";
                const duration = Math.floor(value);
                return [
                    Math.floor(duration / 3600),
                    Math.floor((duration % 3600) / 60),
                    Math.floor(duration % 60),
                ]
                    .map(t => t.toString().padStart(2, "0"))
                    .join(":");
            },
            getMediaMetadata() {
                const dataTag = document.getElementById("player-metadata");
                const metadata = JSON.parse(dataTag?.textContent || "{}");

                if (metadata && Object.keys(metadata).length > 0) {
                    return new MediaMetadata(metadata);
                }
                return null;
            },
            handleError(error) {
                this.pause();
                this.isError = true;
                console.error(error);
            },
        }),
    );
});
