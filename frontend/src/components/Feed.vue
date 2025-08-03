<template>
    <div class="feed-container">
        <h1 class="title" >soon</h1>
        <p class="description">
            prossimamente sarai in grado di vedere i sogni che gli altri condivideranno con te
        </p>
    </div>
</template>
<script>
export default {
    name: 'Feed',
    setup() {
        // Logica per il feed dei sogni
    }
};
</script>
<style>

.feed-container {

    max-width: 800px;
    margin: 0 auto;
    margin-top: 40px;
    padding: 2rem;
    font-family: 'Segoe UI', Arial, sans-serif;
    text-align: center;
    flex: 1;
    background: linear-gradient(135deg, #4b2e83, #6c47a3);
    max-height: 400px;
    border-radius: 16px;
}
</style>