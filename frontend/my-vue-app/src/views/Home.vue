<template>
    <div class="home">
        <section class="hero">
            <h1>Benvenuto su DreamKeeper</h1>
            <p>
                Il tuo spazio personale dove puoi annotare, custodire e rileggere i tuoi sogni.
                Trasforma i tuoi pensieri notturni in ricordi preziosi!
            </p>
            <router-link to="/helloworld" class="cta-button">Inizia ora</router-link>
        </section>
        <section class="features-wrapper">
            <div class="features">
                <h2>Funzionalità principali</h2>
                <ul>
                    <li>📝 Salva e organizza i tuoi sogni in modo semplice e sicuro</li>
                    <li>🔒 Proteggi la tua privacy: solo tu puoi leggere i tuoi sogni</li>
                    <li>📅 Rileggi i tuoi sogni e scopri come cambiano nel tempo</li>
                    <li>🔍 Ricerca tra i tuoi sogni per parole chiave o data</li>
                    <li>🌙 Statistiche sui tuoi sogni più ricorrenti</li>
                    <li>📤 Esporta i tuoi sogni in formato PDF</li>
                </ul>
            </div>
        </section>
        <section class="info-section">
            <h2>Cos'è DreamKeeper?</h2>
            <p>
                DreamKeeper è un diario digitale pensato per aiutarti a ricordare, analizzare e custodire i tuoi sogni. 
                Ogni sogno è importante: annotalo subito dopo il risveglio e rileggilo quando vuoi.
            </p>
            <h3>Perché usare DreamKeeper?</h3>
            <ul>
                <li>✅ Migliora la consapevolezza dei tuoi sogni</li>
                <li>✅ Scopri schemi e temi ricorrenti</li>
                <li>✅ Tutela la tua privacy con un sistema sicuro</li>
            </ul>
        </section>
        <section class="about-section">
            <h2>Chi siamo</h2>
            <p>
                Siamo un piccolo team appassionato di psicologia e tecnologia, con l'obiettivo di aiutare le persone a esplorare il proprio mondo onirico in modo semplice e sicuro.
            </p>
        </section>

        <button class="button">
            hello
        </button>
    </div>
</template>

<script>
export default {
    name: 'Home'
};
</script>

<style scoped>
.home {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Segoe UI', Arial, sans-serif;
}

.hero {
    text-align: center;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #4b2e83;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
}

.cta-button {
    display: inline-block;
    padding: 0.8rem 2rem;
    background: #4b2e83;
    color: #fff;
    border-radius: 25px;
    text-decoration: none;
    font-weight: bold;
    transition: background 1s;
}

.cta-button:hover {
    background: #6c47a3;
}

.features-wrapper {
  background: conic-gradient(#ff00cc, #4b2e83, #ff00cc);
  padding: 5px;
  border-radius: 16px;
  margin-top: 2rem;
}

.features {
  background: rgb(211, 210, 210);
  padding: 1.5rem;
  border-radius: 12px;
}

.features h2 {
    margin-bottom: 1rem;
    color: #4b2e83;
}

.features ul {
    list-style: none;
    padding: 0;
}

.features li {
    color: black;
    margin-bottom: 0.8rem;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
}

.info-section, .about-section {
    background: #f7f6fa;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 2rem;
}

.info-section h2, .about-section h2 {
    color: #4b2e83;
    margin-bottom: 1rem;
}

.info-section h3 {
    color: #6c47a3;
    margin-top: 1.2rem;
    margin-bottom: 0.7rem;
}

.info-section ul {
    list-style: none;
    padding: 0;
}

.info-section li {
    margin-bottom: 0.6rem;
    font-size: 1rem;
    display: flex;
    align-items: center;
}
</style>