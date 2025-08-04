<template>
    <div class="profile-container">
        <div class="profile-card">
            <div class="profile-header">
                <div class="avatar">
                    <span class="avatar-text">{{ userInitials }}</span>
                </div>
                <h2>👤 Il tuo Profilo</h2>
                <p class="welcome-text">Bentornato nel tuo spazio personale, {{ user?.username || 'Utente' }}!</p>
            </div>

            <div class="profile-content">
                <div class="info-section">
                    <h3>📋 Informazioni Personali</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>👤 Nome Utente</label>
                            <div class="info-value">{{ user?.username || 'N/A' }}</div>
                        </div>
                        <div class="info-item">
                            <label>📧 Email</label>
                            <div class="info-value">{{ user?.email || 'N/A' }}</div>
                        </div>
                        <div class="info-item">
                            <label>📅 Membro dal</label>
                            <div class="info-value">{{ formatDate(user?.created_at) }}</div>
                        </div>
                        
                    </div>
                </div>

                <div class="stats-section">
                    <h3>📊 Statistiche</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">{{ dreamCount }}</div>
                            <div class="stat-label">🌙 Sogni Salvati</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ thisMonth }}</div>
                            <div class="stat-label">📆 Sogni ultimo mese</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ thisWeek }}</div>
                            <div class="stat-label">📈 Sogni ultima settimana</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{{ lucid }}</div>
                            <div class="stat-label">📈 Sogni lucidi</div>
                        </div>
                    </div>
                </div>

                <div class="actions-section">
                    <h3>⚙️ Azioni</h3>
                    <div class="action-buttons">
                        <button class="btn btn-primary" @click="editProfile">
                            ✏️ Modifica Profilo
                        </button>
                        <button class="btn btn-secondary" @click="changePassword">
                            🔒 Cambia Password
                        </button>
                        <button class="btn btn-info" @click="exportData">
                            📤 Esporta Dati
                        </button>
                        <button class="btn btn-danger" @click="confirmLogout">
                            🚪 Logout
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal di conferma logout -->
        <div v-if="showLogoutModal" class="modal-overlay" @click="closeLogoutModal">
            <div class="modal-content" @click.stop>
                <h3>🚪 Conferma Logout</h3>
                <p>Sei sicuro di voler uscire dal tuo account?</p>
                <div class="modal-actions">
                    <button class="btn btn-secondary" @click="closeLogoutModal">Annulla</button>
                    <button class="btn btn-danger" @click="logout">Conferma Logout</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useAuth } from '../utils/auth.js'
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api.js'

export default {
    name: 'UserProfile',
    setup() {
        const { store, logout: authLogout } = useAuth()
        const router = useRouter()
        const showLogoutModal = ref(false)

        // Mock data per le statistiche (da sostituire con API reali)
        const dreamCount = ref(0)
        const thisMonth = ref(0)
        const thisWeek = ref(0)
        const lucid = ref(0)

        // Computed properties
        const user = computed(() => {
            const currentUser = store.user
            console.log('User computed:', currentUser)

            // Se non c'è utente autenticato, usa dati demo
            if (!currentUser) {
                return {
                    username: 'Demo User',
                    email: 'demo@dreamkeeper.com',
                    created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
                    updated_at: new Date().toISOString(),
                    is_active: true
                }
            }

            return currentUser
        })

        const userInitials = computed(() => {
            if (!user.value?.username) return 'DU'
            return user.value.username.substring(0, 2).toUpperCase()
        })

        // Methods

        const getUserData = async () => {
            try {
                console.log('Tentativo di chiamata API /me...')

                // Chiamata API per ottenere i dati dell'utente
                const response = await api.get('/api/auth/me')

                console.log('Dati ricevuti:', response.data)

                if (response.data.user) {
                    store.user = response.data.user
                    console.log('Dati utente aggiornati nello store')
                }
            } catch (error) {
                console.error('Errore nel recupero dei dati utente:', error);
                
                // Se è un errore 401, l'utente non è più autenticato
                if (error.response?.status === 401) {
                    console.log('Token scaduto o non valido, effettuo logout')
                    authLogout()
                }
            }
        }

        const getStats = async () => {
            try {
                console.log('Caricamento statistiche utente...')
                const response = await api.get('api/auth/stats')
                console.log('Statistiche ricevute:', response.data)

                // Aggiorna le statistiche
                dreamCount.value = response.data.total || 0
                thisMonth.value = response.data.thisMonth || 0
                thisWeek.value = response.data.thisWeek || 0
                lucid.value = response.data.lucid || 0

            } catch (error) {
                console.error('Errore nel recupero delle statistiche:', error)
                // In caso di errore, mantieni i valori di default (0)
            }
        }

        const formatDate = (dateString) => {
            if (!dateString) return 'N/A'
            const date = new Date(dateString)
            return date.toLocaleDateString('it-IT', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })
        }



        const editProfile = () => {
            // TODO: Implementare modifica profilo
            alert('Funzionalità in arrivo!')
        }

        const changePassword = () => {
            // TODO: Implementare cambio password
            alert('Funzionalità in arrivo!')
        }

        const exportData = () => {
            // TODO: Implementare esportazione dati
            alert('Funzionalità in arrivo!')
        }

        const confirmLogout = () => {
            showLogoutModal.value = true
        }

        const closeLogoutModal = () => {
            showLogoutModal.value = false
        }

        const logout = () => {
            authLogout()
            showLogoutModal.value = false
            router.push('/home')
        }

        // Lifecycle
        onMounted(async () => {
            console.log('Profile.vue montato')

            // Carica dati dall'API se possibile
            await getUserData()
            
            // Carica statistiche utente
            await getStats()

            console.log('Profile.vue completamente inizializzato')
        })

        return {
            user,
            userInitials,
            dreamCount,
            thisMonth,
            thisWeek,
            lucid,
            showLogoutModal,
            getUserData,
            getStats,
            formatDate,
            editProfile,
            changePassword,
            exportData,
            confirmLogout,
            closeLogoutModal,
            logout
        }
    }
}
</script>

<style scoped>
.profile-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: calc(100vh - 120px);
    padding: 2rem;
    flex: 1;
}

.profile-card {
    background: #f7f6fa;
    border-radius: 16px;
    padding: 2rem;
    width: 100%;
    max-width: 800px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border: 2px solid #4b2e83;
    color: #333 !important;
}

.profile-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid #e0e0e0;
}

.avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    box-shadow: 0 4px 12px rgba(75, 46, 131, 0.3);
}

.avatar-text {
    color: white;
    font-size: 1.8rem;
    font-weight: bold;
}

.profile-header h2 {
    color: #4b2e83;
    margin-bottom: 0.5rem;
    font-size: 2rem;
}

.welcome-text {
    color: #666;
    font-size: 1.1rem;
    margin: 0;
}

.profile-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.info-section h3,
.stats-section h3,
.actions-section h3 {
    color: #4b2e83;
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.info-item {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}

.info-item label {
    display: block;
    font-weight: 600;
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.info-value {
    color: #333;
    font-size: 1rem;
}

.status-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    background: #e74c3c;
    color: white;
}

.status-badge.active {
    background: #4caf50;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
}

.stat-card {
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(75, 46, 131, 0.3);
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

.action-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.btn {
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.btn-primary {
    background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
    color: white;
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-info {
    background: #17a2b8;
    color: white;
}

.btn-danger {
    background: #dc3545;
    color: white;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Modal */
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
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 400px;
    width: 90%;
    text-align: center;
}

.modal-content h3 {
    color: #4b2e83;
    margin-bottom: 1rem;
}

.modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
    .profile-container {
        padding: 1rem;
    }

    .profile-card {
        padding: 1.5rem;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .action-buttons {
        grid-template-columns: 1fr;
    }
}
</style>
