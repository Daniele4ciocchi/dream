<template>
    <div class="pomodoro-timer">
        <h1 class="title">Pomodoro Timer</h1>
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

<style>
.pomodoro-timer {
    max-width: 400px;
    margin: auto;
    text-align: center;
    font-family: Arial, sans-serif;
}
.title {
    font-size: 2em;
    margin-bottom: 20px;
    color: rgb(172, 1, 1)
}
.timer-display {
    font-size: 3em;
    margin: 20px 0;
}
.controls button {
    margin: 5px;
    padding: 10px 20px;
    font-size: 1em;
    cursor: pointer;
}
.controls button:disabled {
    background-color: #ccc;
    cursor: not-allowed;        
}
.settings {
    margin-top: 20px;
}
.settings label {
    display: block;
    margin: 10px 0 5px;
}
.settings input {
    width: 100%;
    padding: 8px;
    border-radius: 15px;
}
.settings button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 1em;
    cursor: pointer;
}
.status {
    margin-top: 20px;
    font-size: 1.2em;
}
.status p {
    margin: 5px 0;
}
</style>