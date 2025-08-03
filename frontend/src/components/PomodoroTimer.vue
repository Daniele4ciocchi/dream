<template>
    <div class="pomodoro-container">
        <div class="pomodoro-timer">
            <h1 class="title">Pomodoro Timer</h1>
            <p> 
                se ti stai chiedendo perchè ci sia un pomodoro timer, beh allora fai bene 
                non lo so nemmeno io il perchè, è difficile partire per sviluppare un'applicazione,
                e non sapere dove andare a parare quindi ho deciso di fare un pomodoro timer
            </p>
            <div class="timer-display">
                <span class="time">{{ minutes }}:{{ seconds }}</span>
            </div>
            <div class="controls">
                <button @click="startTimer" :disabled="isRunning">Start</button>
                <button @click="pauseTimer" :disabled="!isRunning">Pause</button>
                <button @click="resetTimer">Stop</button>
            </div>
            <div class="settings">
                <label for="workDuration">Work Duration (minutes):</label>
                <input type="number" id="workDuration" v-model.number="workDuration" min="1" max="60" />
                <label for="breakDuration">Break Duration (minutes):</label>
                <input type="number" id="breakDuration" v-model.number="breakDuration" min="1" max="60" />
                <button @click="resetTimer">set</button>
            </div>
            <div class="status">
                <p v-if="isBreak">Time for a break!</p>
                <p v-else>Keep working!</p>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue';
export default {
    name: 'PomodoroTimer',
    setup() {
        const workDuration = ref(25);
        const breakDuration = ref(5);
        const isRunning = ref(false);
        const isBreak = ref(false);
        const timer = ref(null);
        const timeLeft = ref(workDuration.value * 60);

        const minutes = computed(() => String(Math.floor(timeLeft.value / 60)).padStart(2, '0'));
        const seconds = computed(() => String(timeLeft.value % 60).padStart(2, '0'));

        function startTimer() {
            if (isRunning.value) return;
            isRunning.value = true;
            timer.value = setInterval(() => {
                if (timeLeft.value > 0) {
                    timeLeft.value--;
                } else {
                    toggleMode();
                }
            }, 1000);
        }

        function pauseTimer() {
            clearInterval(timer.value);
            isRunning.value = false;
        }

        function resetTimer() {
            clearInterval(timer.value);
            isRunning.value = false;
            isBreak.value = false;
            timeLeft.value = workDuration.value * 60;
        }

        function toggleMode() {
            isBreak.value = !isBreak.value;
            timeLeft.value = (isBreak.value ? breakDuration.value : workDuration.value) * 60;
        }

        return {
            workDuration,
            breakDuration,
            isRunning,
            isBreak,
            minutes,
            seconds,
            startTimer,
            pauseTimer,
            resetTimer
        };
    }
};

</script>

<style scoped>
.pomodoro-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 120px);
    padding: 2rem;
    flex: 1;
}

.pomodoro-timer {
    max-width: 600px;
    padding: 2rem;
    background: rgba(247, 246, 250, 0.95);
    border-radius: 16px;
    border: 2px solid #4b2e83;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    text-align: center;
    color: #333;
}

.title {
    color: #4b2e83;
    margin-bottom: 30px;
}

.timer-display {
    margin: 20px 0;
}

.time {
    font-size: 3rem;
    font-weight: bold;
    color: #4b2e83;
}

.controls {
    margin: 20px 0;
}

.controls button {
    margin: 5px;
    padding: 12px 24px;
    font-size: 1em;
    cursor: pointer;
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    color: white;
    border: none;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.controls button:hover:not(:disabled) {
    background: linear-gradient(135deg, #5d3a99 0%, #7d57b3 100%);
    transform: translateY(-2px);
}

.controls button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
    transform: none;
}

.settings {
    margin-top: 20px;
}

.settings label {
    display: block;
    margin: 10px 0 5px;
    color: #4b2e83;
    font-weight: 500;
}

.settings input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  max-width: 200px;
  background: white !important;
  color: #333 !important;
}

.settings input::placeholder {
  color: #999 !important;
}.settings input:focus {
    outline: none;
    border-color: #4b2e83;
}

.settings button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 1em;
    cursor: pointer;
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    color: white;
    border: none;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.settings button:hover {
    background: linear-gradient(135deg, #5d3a99 0%, #7d57b3 100%);
}

.status {
    margin-top: 20px;
    font-size: 1.2em;
    color: #4b2e83;
    font-weight: 500;
}

.status p {
    margin: 5px 0;
}
</style>