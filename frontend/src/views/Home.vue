<template>
    <div class="home">
        <!-- Hero Section with animated background -->
        <section class="hero">
            <div class="hero-background">
                <div class="floating-dreams"></div>
                <div class="aurora"></div>
                <div class="falling-stars"></div>
            </div>
            <div class="hero-content">
                <div class="hero-icon">🌙</div>
                <h1 v-if="!isAuthenticated">Benvenuto su <span class="brand">DreamKeeper</span></h1>
                <h1 v-else>Bentornato, <span class="brand">{{ user?.username }}!</span></h1>
                <p class="hero-subtitle" v-if="!isAuthenticated">
                    Il tuo spazio personale dove puoi annotare, custodire e rileggere i tuoi sogni.
                    <br>Trasforma i tuoi pensieri notturni in ricordi preziosi!
                </p>
                <p class="hero-subtitle" v-else>
                    È il momento di aggiungere un nuovo capitolo al tuo diario dei sogni!
                    <br>Cosa hai sognato stanotte? ✨
                </p>
                <div class="cta-group" v-if="!isAuthenticated">
                    <router-link to="/register" class="cta-button primary">
                        ✨ Registrati Gratis
                    </router-link>
                    <router-link to="/login" class="cta-button secondary">
                        🔐 Accedi
                    </router-link>
                </div>
                <div class="cta-group" v-else>
                    <router-link to="/my-dreams" class="cta-button primary">
                        📖 I Miei Sogni
                    </router-link>
                    <button @click="openQuickAddModal" class="cta-button secondary">
                        ➕ Aggiungi Sogno
                    </button>
                </div>
            </div>
        </section>

        <!-- Features Section with cards -->
        <section class="features-section">
            <div class="section-header">
                <h2>🌟 Funzionalità principali</h2>
                <p>Scopri tutto quello che puoi fare con DreamKeeper</p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">📝</div>
                    <h3>Salva i tuoi sogni</h3>
                    <p>Organizza i tuoi sogni in modo semplice e sicuro con il nostro editor intuitivo</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Privacy garantita</h3>
                    <p>Solo tu puoi leggere i tuoi sogni. La tua privacy è la nostra priorità</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📅</div>
                    <h3>Analisi temporale</h3>
                    <p>Rileggi i tuoi sogni e scopri come cambiano nel tempo</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔍</div>
                    <h3>Ricerca avanzata</h3>
                    <p>Trova facilmente i tuoi sogni per parole chiave, data o mood</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🌙</div>
                    <h3>Statistiche oniriche</h3>
                    <p>Scopri i pattern e i temi ricorrenti nei tuoi sogni</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📤</div>
                    <h3>Esporta tutto</h3>
                    <p>Scarica i tuoi sogni in formato PDF per conservarli per sempre</p>
                </div>
            </div>
        </section>

        <!-- Info Section -->
        <section class="info-section">
            <div class="info-content">
                <div class="info-text">
                    <h2>💭 Cos'è DreamKeeper?</h2>
                    <p>
                        DreamKeeper è un diario digitale pensato per aiutarti a ricordare, analizzare e custodire i tuoi
                        sogni.
                        Ogni sogno è importante: annotalo subito dopo il risveglio e rileggilo quando vuoi.
                    </p>
                    <h3>✨ Perché usare DreamKeeper?</h3>
                    <div class="benefits-list">
                        <div class="benefit-item">
                            <span class="benefit-icon">🧠</span>
                            <span>Migliora la consapevolezza dei tuoi sogni</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">🔍</span>
                            <span>Scopri schemi e temi ricorrenti</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">🛡️</span>
                            <span>Tutela la tua privacy con un sistema sicuro</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">🔬</span>
                            <span>Approccio scientifico ai sogni</span>
                        </div>
                    </div>
                </div>
                <div class="info-visual">
                    <div class="dream-cloud">
                        <div class="cloud-text">I tuoi sogni<br>sono al sicuro</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Call to Action Footer -->
        <section class="cta-footer" v-if="!isAuthenticated">
            <div class="cta-content">
                <h2>🚀 Pronto a iniziare il tuo viaggio nei sogni?</h2>
                <p>Unisciti a migliaia di persone che stanno già esplorando il loro mondo onirico</p>
                <div class="cta-actions">
                    <router-link to="/register" class="cta-button primary large">
                        ✨ Registrati gratuitamente
                    </router-link>
                    
                    <!-- PayPal Donate Button Styled -->
                    <div class="support-section">
                        <p class="support-text">Ti piace DreamKeeper? Sostienici!</p>
                        <form action="https://www.paypal.com/donate" method="post" target="_top" class="paypal-form">
                            <input type="hidden" name="hosted_button_id" value="QEPY9GYEUQH4A" />
                            <button type="submit" class="paypal-button">
                                <span class="paypal-icon">💝</span>
                                <span class="paypal-text">Sostieni il progetto</span>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </section>

    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '../utils/auth.js'
import { useRouter } from 'vue-router'
import api from '../utils/api.js'

export default {
    name: 'Home',
    setup() {
        const { user, isAuthenticated } = useAuth()
        const router = useRouter()

        const showQuickModal = ref(false)
        const submitting = ref(false)
        const dreamStats = ref({
            total: 0,
            thisMonth: 0,
            lucid: 0
        })

        const quickDream = ref({
            title: '',
            content: ''
        })

        // Fetch user dream statistics if authenticated
        const fetchDreamStats = async () => {
            if (!isAuthenticated.value) return

            try {
                const response = await api.get('/api/dreams/stats')
                dreamStats.value = response.data
            } catch (error) {
                console.error('Errore nel recupero delle statistiche:', error)
            }
        }

        const openQuickAddModal = () => {
            showQuickModal.value = true
            quickDream.value = { title: '', content: '' }
        }

        const closeQuickModal = () => {
            showQuickModal.value = false
        }

        const quickSaveDream = async () => {
            if (submitting.value) return

            submitting.value = true

            try {
                const dreamData = {
                    title: quickDream.value.title.trim(),
                    content: quickDream.value.content.trim(),
                    date_dreamed: new Date().toISOString().split('T')[0],
                    is_private: true
                }

                await api.post('/api/dreams', dreamData)

                closeQuickModal()

                // Redirect to dreams page
                router.push('/my-dreams')

            } catch (error) {
                console.error('Errore nel salvare il sogno:', error)
                // Gestione silente dell'errore
            } finally {
                submitting.value = false
            }
        }

        onMounted(() => {
            fetchDreamStats()
        })

        return {
            user,
            isAuthenticated,
            showQuickModal,
            submitting,
            dreamStats,
            quickDream,
            openQuickAddModal,
            closeQuickModal,
            quickSaveDream
        }
    }
}
</script>

<style scoped>
.home {
    min-height: 100vh;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    line-height: 1.6;
    color: #2d3748;
}

/* Hero Section */
.hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;

    overflow: hidden;
}

.hero-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 30% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
    animation: subtleFloat 8s ease-in-out infinite;
}

@keyframes subtleFloat {

    0%,
    100% {
        transform: translateY(0px);
        opacity: 0.3;
    }

    50% {
        transform: translateY(-20px);
        opacity: 0.6;
    }
}

.aurora {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg,
            transparent 40%,
            rgba(255, 255, 255, 0.05) 50%,
            transparent 60%);
    animation: gentleMove 10s ease-in-out infinite;
}

@keyframes gentleMove {

    0%,
    100% {
        transform: translateX(-30px);
        opacity: 0.5;
    }

    50% {
        transform: translateX(30px);
        opacity: 0.8;
    }
}

.floating-dreams {
    position: absolute;
    width: 100%;
    height: 100%;
    background-image:
        radial-gradient(2px 2px at 40px 60px, rgba(255, 255, 255, 0.2), transparent),
        radial-gradient(1px 1px at 80px 40px, rgba(255, 255, 255, 0.3), transparent);
    background-repeat: repeat;
    background-size: 200px 150px;
    animation: slowFloat 15s infinite linear;
}

.falling-stars {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.falling-stars::before,
.falling-stars::after {
    content: '';
    position: absolute;
    width: 2px;
    height: 2px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    box-shadow:
        0 0 6px rgba(255, 255, 255, 0.8),
        0 0 12px rgba(255, 255, 255, 0.6),
        0 0 18px rgba(255, 255, 255, 0.4);
}

.falling-stars::before {
    left: 15%;
    animation: fallingStar1 7s linear infinite;
    animation-delay: 0s;
}

.falling-stars::after {
    left: 75%;
    animation: fallingStar2 9s linear infinite;
    animation-delay: 2s;
}

/* Aggiungiamo più stelle usando pseudo-elementi aggiuntivi */
.hero-background::before,
.hero-background::after {
    content: '';
    position: absolute;
    width: 1.5px;
    height: 1.5px;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    box-shadow:
        0 0 4px rgba(255, 255, 255, 0.6),
        0 0 8px rgba(255, 255, 255, 0.4);
}

.hero-background::before {
    left: 35%;
    animation: fallingStar3 11s linear infinite;
    animation-delay: 4s;
}

.hero-background::after {
    left: 60%;
    animation: fallingStar4 6s linear infinite;
    animation-delay: 7s;
}

/* Animazioni casuali diverse per ogni stella */
@keyframes fallingStar1 {
    0% {
        top: -10px;
        opacity: 0;
        transform: translateX(0px);
    }

    10% {
        opacity: 1;
    }

    90% {
        opacity: 1;
    }

    100% {
        top: 100vh;
        opacity: 0;
        transform: translateX(80px);
    }
}

@keyframes fallingStar2 {
    0% {
        top: -10px;
        opacity: 0;
        transform: translateX(0px);
    }

    15% {
        opacity: 1;
    }

    85% {
        opacity: 1;
    }

    100% {
        top: 100vh;
        opacity: 0;
        transform: translateX(-60px);
    }
}

@keyframes fallingStar3 {
    0% {
        top: -10px;
        opacity: 0;
        transform: translateX(0px);
    }

    20% {
        opacity: 1;
    }

    80% {
        opacity: 1;
    }

    100% {
        top: 100vh;
        opacity: 0;
        transform: translateX(120px);
    }
}

@keyframes fallingStar4 {
    0% {
        top: -10px;
        opacity: 0;
        transform: translateX(0px);
    }

    25% {
        opacity: 1;
    }

    75% {
        opacity: 1;
    }

    100% {
        top: 100vh;
        opacity: 0;
        transform: translateX(-40px);
    }
}

@keyframes slowFloat {
    0% {
        transform: translateY(0px);
    }

    100% {
        transform: translateY(-50px);
    }
}

.hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
    max-width: 800px;
    padding: 2rem;
    color: white;
}

.hero-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    animation: gentlePulse 3s ease-in-out infinite;
}

@keyframes gentlePulse {

    0%,
    100% {
        transform: scale(1);
        opacity: 0.9;
    }

    50% {
        transform: scale(1.05);
        opacity: 1;
    }
}

.hero h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.brand {
    background: linear-gradient(45deg, #feca57, #ff9ff3, #48dbfb);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: smoothGradient 4s ease-in-out infinite;
}

@keyframes smoothGradient {

    0%,
    100% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }
}

.hero-subtitle {
    font-size: 1.3rem;
    margin-bottom: 2.5rem;
    opacity: 0.9;
    text-shadow: 0 1px 10px rgba(0, 0, 0, 0.2);
}

.cta-group {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.cta-button {
    display: inline-flex;
    align-items: center;
    padding: 1rem 2rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    border: none;
    cursor: pointer;
}

.cta-button.primary {
    background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
    color: white;
}

.cta-button.secondary {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
}

.cta-button.large {
    padding: 1.2rem 2.5rem;
    font-size: 1.2rem;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

/* Features Section */
.features-section {
    padding: 6rem 2rem;
    background: linear-gradient(180deg, #f8fafc 0%, #edf2f7 100%);
}

.section-header {
    text-align: center;
    max-width: 600px;
    margin: 0 auto 4rem;
}

.section-header h2 {
    font-size: 2.5rem;
    color: #2d3748;
    margin-bottom: 1rem;
}

.section-header p {
    font-size: 1.2rem;
    color: #718096;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.feature-card {
    background: white;
    padding: 2.5rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    border-color: rgba(102, 126, 234, 0.2);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    display: block;
    transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
    transform: scale(1.1);
}

.feature-card h3 {
    font-size: 1.5rem;
    color: #2d3748;
    margin-bottom: 1rem;
    font-weight: 600;
    transition: color 0.3s ease;
}

.feature-card:hover h3 {
    color: #667eea;
}

.feature-card p {
    color: #718096;
    font-size: 1.1rem;
    line-height: 1.6;
}

/* Info Section */
.info-section {
    padding: 6rem 2rem;
    background: white;
}

.info-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    max-width: 1200px;
    margin: 0 auto;
    align-items: center;
}

.info-text h2 {
    font-size: 2.5rem;
    color: #2d3748;
    margin-bottom: 1.5rem;
}

.info-text p {
    font-size: 1.2rem;
    color: #718096;
    margin-bottom: 2rem;
}

.info-text h3 {
    font-size: 1.8rem;
    color: #4c51bf;
    margin-bottom: 1.5rem;
}

.benefits-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.benefit-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1.1rem;
    color: #2d3748;
}

.benefit-icon {
    font-size: 1.5rem;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    color: white;
}

.info-visual {
    display: flex;
    justify-content: center;
    align-items: center;
}

.dream-cloud {
    width: 300px;
    height: 200px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.3rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    animation: cloudFloat 3s ease-in-out infinite;
}

@keyframes cloudFloat {

    0%,
    100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }
}

/* PayPal Support Section */

/* CTA Footer */
.cta-footer {
    padding: 6rem 2rem;
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    color: white;
    text-align: center;
}

.cta-content h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.cta-content p {
    font-size: 1.2rem;
    margin-bottom: 2.5rem;
    opacity: 0.9;
}

.cta-actions {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
}

/* PayPal Support Section */
.support-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.support-text {
    font-size: 1rem;
    opacity: 0.8;
    margin: 0;
}

.paypal-form {
    margin: 0;
    padding: 0;
}

.paypal-button {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.8rem 1.8rem;
    border: none;
    border-radius: 25px;
    background: linear-gradient(135deg, #0070ba 0%, #003087 100%);
    color: white;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 112, 186, 0.3);
    font-family: inherit;
}

.paypal-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 112, 186, 0.4);
    background: linear-gradient(135deg, #0079c1 0%, #003f96 100%);
}

.paypal-button:active {
    transform: translateY(0);
}

.paypal-icon {
    font-size: 1.2rem;
    animation: heartbeat 2s ease-in-out infinite;
}

@keyframes heartbeat {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

.paypal-text {
    font-size: 1rem;
    letter-spacing: 0.5px;
}

/* Stats Section */
.stats-section {
    padding: 6rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
}

.stats-content h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.stats-content p {
    font-size: 1.2rem;
    margin-bottom: 3rem;
    opacity: 0.9;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto 3rem;
}

.stat-card {
    background: rgba(255, 255, 255, 0.15);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.stat-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    animation: gentleFloat 3s ease-in-out infinite;
}

@keyframes gentleFloat {

    0%,
    100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-5px);
    }
}

.stat-number {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(45deg, #feca57, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 1rem;
    opacity: 0.9;
}

@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(30px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Quick Modal */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(5px);
}

.quick-modal {
    background: white;
    border-radius: 20px;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    animation: modalAppear 0.3s ease-out;
}

@keyframes modalAppear {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(20px);
    }

    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

.modal-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
    font-size: 1.3rem;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    transition: all 0.2s ease;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1);
}

.quick-form {
    padding: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 1rem;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.2s ease;
    font-family: inherit;
    resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    transform: translateY(-1px);
}

.quick-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
}

.btn-cancel,
.btn-save {
    padding: 0.8rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    font-size: 1rem;
}

.btn-cancel {
    background: #f7fafc;
    color: #4a5568;
    border: 1px solid #e2e8f0;
}

.btn-cancel:hover {
    background: #edf2f7;
    transform: translateY(-1px);
}

.btn-save {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-save:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.btn-save:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero {
        min-height: 90vh;
    }

    .hero h1 {
        font-size: 2.8rem;
    }

    .hero-subtitle {
        font-size: 1.2rem;
    }

    .hero-icon {
        font-size: 4rem;
    }

    .cta-group {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .cta-button {
        width: 80%;
        justify-content: center;
    }

    .features-grid {
        grid-template-columns: 1fr;
        gap: 2rem;
    }

    .feature-card {
        padding: 2.5rem;
    }

    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
    }

    .info-content {
        grid-template-columns: 1fr;
        gap: 3rem;
    }

    .stats-grid {
        grid-template-columns: 1fr;
        gap: 2rem;
    }

    .team-values {
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }

    .cta-actions {
        gap: 1.5rem;
    }

    .paypal-button {
        padding: 0.7rem 1.5rem;
        font-size: 0.9rem;
    }

    .section-header h2,
    .info-text h2,
    .cta-content h2,
    .stats-content h2 {
        font-size: 2.2rem;
    }

    .features-section,
    .info-section,
    .cta-footer,
    .stats-section {
        padding: 5rem 1.5rem;
    }
}

@media (max-width: 480px) {
    .hero {
        min-height: 85vh;
    }

    .hero h1 {
        font-size: 2.2rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
    }

    .hero-icon {
        font-size: 3.5rem;
    }

    .cta-button {
        padding: 1rem 2rem;
        font-size: 1.1rem;
    }

    .feature-card {
        padding: 2rem;
    }

    .feature-icon {
        font-size: 3rem;
    }

    .stat-number {
        font-size: 3rem;
    }

    .stat-icon {
        font-size: 2.5rem;
    }

    .section-header h2,
    .stats-content h2 {
        font-size: 1.8rem;
    }
}

/* Scroll animations */
@media (prefers-reduced-motion: no-preference) {

    .feature-card,
    .stat-card {
        animation: slideInUp 0.8s ease-out both;
    }

    .feature-card:nth-child(1) {
        animation-delay: 0.1s;
    }

    .feature-card:nth-child(2) {
        animation-delay: 0.2s;
    }

    .feature-card:nth-child(3) {
        animation-delay: 0.3s;
    }

    .feature-card:nth-child(4) {
        animation-delay: 0.4s;
    }

    .feature-card:nth-child(5) {
        animation-delay: 0.5s;
    }

    .feature-card:nth-child(6) {
        animation-delay: 0.6s;
    }
}

@keyframes slideInUp {
    0% {
        opacity: 0;
        transform: translateY(50px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Enhanced glassmorphism effects */
.quick-modal {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Performance optimizations */
.floating-dreams,
.aurora,
.hero-background,
.falling-stars {
    will-change: transform;
}

.feature-card,
.stat-card,
.cta-button {
    will-change: transform;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .feature-card {
        background: linear-gradient(145deg, #2d3748 0%, #4a5568 100%);
        color: white;
    }

    .feature-card h3 {
        color: #e2e8f0;
    }

    .feature-card:hover h3 {
        color: #90cdf4;
    }

    .feature-card p {
        color: #a0aec0;
    }

    .feature-card:hover p {
        color: #cbd5e0;
    }
}
</style>