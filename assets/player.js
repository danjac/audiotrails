document.addEventListener('alpine:init', () => {
    /* initialize any Alpine components here */
    window.Alpine.data(
        'player',
        (
            autoplay = false,
            mediaSrc = null,
            currentTime = 0,
            timeUpdateUrl = null,
            csrfToken = null
        ) => ({
            autoplay,
            mediaSrc,
            currentTime,
            csrfToken,
            timeUpdateUrl,
            duration: 0,
            isError: false,
            isLoaded: false,
            isPaused: false,
            isPlaying: false,
            playbackRate: 1.0,
            defaultPlaybackRate: 1.0,
            lastTimeUpdate: null,
            counters: {
                current: '00:00:00',
                duration: '00:00:00',
            },
            init() {
                this.$watch('currentTime', (value) => {
                    this.counters.current = this.formatDuration(value);
                });

                this.$watch('duration', (value) => {
                    this.counters.duration = this.formatDuration(value);
                });

                this.$watch('playbackRate', (value) => {
                    this.$refs.audio.playbackRate = value;
                });

                this.counters.current = this.formatDuration(this.currentTime);
                this.counters.duration = this.formatDuration(this.duration);

                this.$refs.audio.currentTime = this.currentTime;
                this.$refs.audio.load();

                if ('mediaSession' in navigator) {
                    navigator.mediaSession.metadata = this.getMediaMetadata();
                }
            },
            get isInteractive() {
                return this.isPlaying && !this.isError;
            },
            formatDuration(value) {
                if (isNaN(value) || value < 0) return '00:00:00';
                const duration = Math.floor(value);
                const hours = Math.floor(duration / 3600);
                const minutes = Math.floor((duration % 3600) / 60);
                const seconds = Math.floor(duration % 60);
                return [hours, minutes, seconds]
                    .map((t) => t.toString().padStart(2, '0'))
                    .join(':');
            },
            getMediaMetadata() {
                const dataTag = document.getElementById('player-metadata');
                if (!dataTag) {
                    return null;
                }

                const metadata = JSON.parse(dataTag.textContent);

                if (metadata && Object.keys(metadata).length > 0) {
                    return new window.MediaMetadata(metadata);
                }
                return null;
            },
            shortcuts(event) {
                if (event.target.tagName.match(/INPUT|TEXTAREA/)) {
                    return;
                }

                if (!event.ctrlKey && !event.altKey) {
                    switch (event.code) {
                        case 'Space':
                            event.preventDefault();
                            event.stopPropagation();
                            this.togglePlayPause();
                            return;
                        case 'ArrowRight':
                            event.preventDefault();
                            event.stopPropagation();
                            this.skipForward();
                            return;
                        case 'ArrowLeft':
                            event.preventDefault();
                            event.stopPropagation();
                            this.skipBack();
                            return;
                    }
                }

                // playback rate
                if (event.altKey) {
                    switch (event.key) {
                        case '+':
                            event.preventDefault();
                            event.stopPropagation();
                            this.incrementPlaybackRate();
                            return;
                        case '-':
                            event.preventDefault();
                            event.stopPropagation();
                            this.decrementPlaybackRate();
                            return;
                        case '0':
                            event.preventDefault();
                            event.stopPropagation();
                            this.resetPlaybackRate();
                            return;
                    }
                }
            },
            loaded() {
                if (this.isLoaded) {
                    return;
                }

                this.isError = false;

                const { playbackRate, autoplay } = this.restore();

                this.playbackRate = playbackRate || this.defaultPlaybackRate;
                this.autoplay = this.autoplay || autoplay;

                if (this.autoplay) {
                    this.$refs.audio.play().catch(() => {
                        this.isPaused = true;
                        this.isPlaying = false;
                        this.isError = true;
                    });
                } else {
                    this.isPaused = true;
                    this.isPlaying = false;
                }

                this.duration = this.$refs.audio.duration;
                this.isLoaded = true;
            },
            error() {
                this.isPlaying = false;
                this.isError = true;
            },
            timeUpdate() {
                this.isPlaying = true;
                this.currentTime = Math.floor(this.$refs.audio.currentTime);
                const time = Math.round(this.currentTime);
                if (time % 5 === 0 && this.lastTimeUpdate !== time) {
                    this.lastTimeUpdate = time;
                    fetch(this.timeUpdateUrl, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': this.csrfToken,
                        },
                        body: new URLSearchParams({
                            current_time: time,
                        }),
                    });
                }
            },
            buffering() {
                this.isPlaying = false;
            },
            resumed() {
                this.isPaused = false;
                this.isPlaying = true;
                this.isError = false;
                this.store();
            },
            paused() {
                this.isPlaying = false;
                this.isPaused = true;
                this.store();
            },
            incrementPlaybackRate() {
                this.changePlaybackRate(0.1);
            },
            decrementPlaybackRate() {
                this.changePlaybackRate(-0.1);
            },
            resetPlaybackRate() {
                this.setPlaybackRate(this.defaultPlaybackRate);
            },
            changePlaybackRate(increment) {
                const newValue = Math.max(
                    0.5,
                    Math.min(2.0, parseFloat(this.playbackRate) + increment)
                );
                this.setPlaybackRate(newValue);
            },
            setPlaybackRate(value) {
                this.playbackRate = value;
                this.store();
            },
            restore() {
                const stored = sessionStorage.getItem('player');
                return stored
                    ? JSON.parse(stored)
                    : {
                          playbackRate: this.defaultPlaybackRate,
                          autoplay: false,
                      };
            },
            store() {
                sessionStorage.setItem(
                    'player',
                    JSON.stringify({
                        playbackRate: this.playbackRate,
                        autoplay: this.isPlaying,
                    })
                );
            },
            skip() {
                if (!this.isPaused) {
                    this.$refs.audio.currentTime = this.currentTime;
                }
            },
            skipBack() {
                if (!this.isPaused) {
                    this.$refs.audio.currentTime -= 10;
                }
            },
            skipForward() {
                if (!this.isPaused) {
                    this.$refs.audio.currentTime += 10;
                }
            },
            ended() {
                this.$refs.complete.click();
            },
            togglePlayPause() {
                if (this.isPaused) {
                    this.$refs.audio.play();
                } else {
                    this.$refs.audio.pause();
                }
            },
        })
    );
});
