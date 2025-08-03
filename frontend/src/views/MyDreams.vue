<template>
  <div class="dreams-container">
    <div class="dreams-header">
      <h1>🌙 I Miei Sogni</h1>
      <p>Qui troverai tutti i tuoi sogni salvati nel tempo.</p>
      <button class="btn btn-primary add-dream-btn" @click="openAddDreamModal">
        ➕ Aggiungi Nuovo Sogno
      </button>
    </div>

    <div class="dreams-content" v-if="dreams.length > 0">
      <ul class="dream-list">
        <li class="dream-item" v-for="dream in dreams" :key="dream.id">
          <h3>{{ dream.title }}</h3>
          <p>{{ dream.content }}</p>
          <small>{{ dream.date_dreamed }} - {{ dream.mood || 'Nessun mood' }}</small>
          <div class="dream-actions">
            <button class="btn btn-edit" @click="openEditDreamModal(dream)">
              ✏️ Modifica
            </button>
            <button class="btn btn-danger" @click="deleteDream(dream.id)">
              🗑️ Elimina Sogno
            </button>
          </div>
        </li>
      </ul>
    </div>

    <div class="dreams-content" v-else>
      <div class="empty-state">
        <div class="empty-icon">💭</div>
        <h3>Nessun sogno ancora</h3>
        <p>Non hai ancora salvato nessun sogno. Inizia a registrare i tuoi sogni per costruire il tuo diario onirico!</p>
        <button class="btn" @click="openAddDreamModal">
          ✨ Aggiungi il primo sogno
        </button>
      </div>
    </div>

    <!-- Modal per aggiungere/modificare sogno -->
    <div class="modal-overlay" v-if="showAddDreamModal" @click="closeAddDreamModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ isEditMode ? '✏️ Modifica Sogno' : '✨ Aggiungi Nuovo Sogno' }}</h2>
          <button class="close-btn" @click="closeAddDreamModal">&times;</button>
        </div>
        
        <form @submit.prevent="submitDream" class="dream-form">
          <div class="form-group">
            <label for="title">📝 Titolo del Sogno *</label>
            <input 
              type="text" 
              id="title" 
              v-model="dreamForm.title" 
              placeholder="Es: Il volo magico, La casa misteriosa..."
              required
              maxlength="200"
            >
          </div>

          <div class="form-group">
            <label for="content">📖 Descrizione del Sogno *</label>
            <textarea 
              id="content" 
              v-model="dreamForm.content" 
              placeholder="Racconta il tuo sogno in dettaglio..."
              required
              rows="6"
              maxlength="5000"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="date_dreamed">📅 Data del Sogno *</label>
              <input 
                type="date" 
                id="date_dreamed" 
                v-model="dreamForm.date_dreamed" 
                required
              >
            </div>

            <div class="form-group">
              <label for="mood">😊 Stato d'Animo</label>
              <select id="mood" v-model="dreamForm.mood">
                <option value="">Seleziona uno stato d'animo</option>
                <option value="happy">😊 Felice</option>
                <option value="scared">😨 Spaventato</option>
                <option value="mysterious">🔮 Misterioso</option>
                <option value="exciting">🎉 Eccitante</option>
                <option value="peaceful">😌 Sereno</option>
                <option value="weird">🤪 Strano</option>
                <option value="sad">😢 Triste</option>
                <option value="adventurous">🗺️ Avventuroso</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="tags">🏷️ Tag (separati da virgola)</label>
            <input 
              type="text" 
              id="tags" 
              v-model="dreamForm.tags" 
              placeholder="Es: volo, montagne, famiglia, animali..."
            >
            <small>Inserisci parole chiave separate da virgola per categorizzare il sogno</small>
          </div>

          <div class="form-row">
            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="dreamForm.is_lucid"
                >
                <span class="checkmark"></span>
                🌟 Era un sogno lucido?
              </label>
              <small>Un sogno lucido è quando ti rendi conto di stare sognando</small>
            </div>

            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="dreamForm.is_private"
                >
                <span class="checkmark"></span>
                🔒 Mantieni privato
              </label>
              <small>Solo tu potrai vedere questo sogno</small>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeAddDreamModal">
              Annulla
            </button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? (isEditMode ? 'Aggiornando...' : 'Salvando...') : (isEditMode ? '💾 Aggiorna Sogno' : '💾 Salva Sogno') }}
            </button>
          </div>
        </form>
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
  name: 'MyDreams',
  setup() {
    const { logout } = useAuth();
    const router = useRouter();
    const dreams = ref([]);
    const showAddDreamModal = ref(false);
    const submitting = ref(false);
    const isEditMode = ref(false);
    const editingDreamId = ref(null);
    
    // Form data per il nuovo sogno
    const dreamForm = ref({
      title: '',
      content: '',
      date_dreamed: new Date().toISOString().split('T')[0], // Data di oggi
      mood: '',
      tags: '',
      is_lucid: false,
      is_private: true
    });

    const getDreams = async () => {
      try {
        const response = await api.get('/api/dreams');
        console.log('Risposta completa dal backend:', response.data);
        
        // Il backend restituisce {dreams: [...], pagination: {...}}
        if (response.data && response.data.dreams) {
          dreams.value = response.data.dreams;
        } else {
          dreams.value = [];
        }
        
        console.log('Sogni recuperati:', dreams.value);
      } catch (error) {
        console.error('Errore nel recupero dei sogni:', error);
        console.error('Status:', error.response?.status);
        console.error('Message:', error.response?.data?.message);
        console.error('Errore completo:', error.response?.data);
        
        // Se è un errore 401, l'utente non è più autenticato
        if (error.response?.status === 401) {
          console.log('Token scaduto o non valido, effettuo logout');
          logout();
          router.push('/login');
        }
      }
    };

    const deleteDream = async (dreamId) => {
      if (!confirm('Sei sicuro di voler eliminare questo sogno?')) return;

      try {
        await api.delete(`/api/dreams/${dreamId}`);
        console.log(`Sogno ${dreamId} eliminato con successo`);
        
        // Ricarica la lista dei sogni
        await getDreams();
        
      } catch (error) {
        console.error('Errore nell\'eliminazione del sogno:', error);
        console.error('Status:', error.response?.status);
        console.error('Message:', error.response?.data?.message);
        console.error('Errore completo:', error.response?.data);
        
        // Se è un errore 401, logout
        if (error.response?.status === 401) {
          logout();
          router.push('/login');
        }
      }
    };

    const openAddDreamModal = () => {
      isEditMode.value = false;
      editingDreamId.value = null;
      showAddDreamModal.value = true;
      // Reset del form
      dreamForm.value = {
        title: '',
        content: '',
        date_dreamed: new Date().toISOString().split('T')[0],
        mood: '',
        tags: '',
        is_lucid: false,
        is_private: true
      };
    };

    const openEditDreamModal = (dream) => {
      isEditMode.value = true;
      editingDreamId.value = dream.id;
      showAddDreamModal.value = true;
      // Popola il form con i dati del sogno esistente
      dreamForm.value = {
        title: dream.title,
        content: dream.content,
        date_dreamed: dream.date_dreamed,
        mood: dream.mood || '',
        tags: dream.tags ? (Array.isArray(dream.tags) ? dream.tags.join(', ') : dream.tags) : '',
        is_lucid: dream.is_lucid || false,
        is_private: dream.is_private !== undefined ? dream.is_private : true
      };
    };

    const closeAddDreamModal = () => {
      showAddDreamModal.value = false;
      isEditMode.value = false;
      editingDreamId.value = null;
    };

    const submitDream = async () => {
      if (submitting.value) return;
      
      submitting.value = true;
      
      try {
        // Prepara i dati per l'invio
        const dreamData = {
          title: dreamForm.value.title.trim(),
          content: dreamForm.value.content.trim(),
          date_dreamed: dreamForm.value.date_dreamed,
          mood: dreamForm.value.mood || null,
          is_lucid: dreamForm.value.is_lucid,
          is_private: dreamForm.value.is_private,
          tags: dreamForm.value.tags ? dreamForm.value.tags.split(',').map(tag => tag.trim()).filter(tag => tag) : []
        };

        console.log('Invio dati sogno:', dreamData);
        console.log('Modalità:', isEditMode.value ? 'Modifica' : 'Creazione');

        let response;
        if (isEditMode.value) {
          // Aggiorna sogno esistente
          response = await api.put(`/api/dreams/${editingDreamId.value}`, dreamData);
          console.log('Sogno aggiornato:', response.data);
          alert('Sogno aggiornato con successo! ✨');
        } else {
          // Crea nuovo sogno
          response = await api.post('/api/dreams', dreamData);
          console.log('Sogno creato:', response.data);
          alert('Sogno salvato con successo! 🌟');
        }
        
        // Chiudi il modal
        closeAddDreamModal();
        
        // Ricarica la lista dei sogni
        await getDreams();
        
      } catch (error) {
        console.error('Errore nel salvare/aggiornare il sogno:', error);
        console.error('Status:', error.response?.status);
        console.error('Message:', error.response?.data?.message);
        console.error('Errore completo:', error.response?.data);
        
        // Mostra messaggio di errore più dettagliato
        let errorMessage = isEditMode.value ? 'Errore nell\'aggiornare il sogno' : 'Errore nel salvare il sogno';
        if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        } else if (error.response?.data?.errors) {
          errorMessage = 'Errori di validazione: ' + JSON.stringify(error.response.data.errors);
        }
        
        alert(errorMessage);
        
        // Se è un errore 401, logout
        if (error.response?.status === 401) {
          logout();
          router.push('/login');
        }
      } finally {
        submitting.value = false;
      }
    };

    onMounted(async () => {
      await getDreams();
    });

    // IMPORTANTE: Restituisci tutto quello che vuoi usare nel template
    return {
      dreams,
      showAddDreamModal,
      dreamForm,
      submitting,
      isEditMode,
      editingDreamId,
      getDreams,
      deleteDream,
      openAddDreamModal,
      openEditDreamModal,
      closeAddDreamModal,
      submitDream
    };
  }
}

</script>

<style scoped>
.dreams-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  flex: 1;
}

.dreams-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dreams-header h1 {
  color: #4b2e83;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.dreams-header p {
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.add-dream-btn {
  background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-dream-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(75, 46, 131, 0.3);
}

.dreams-content {
  background: #f7f6fa;
  border-radius: 16px;
  padding: 3rem;
  border: 2px solid #4b2e83;
  min-height: 400px;
  min-width: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #4b2e83;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2rem;
  max-width: 400px;
}

.btn {
  background: linear-gradient(135deg, #4b2e83 0%, #6c47a3 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(75, 46, 131, 0.3);
}

.dream-list {
  list-style: none;
  padding: 0;
  width: 100%;
}

.dream-item {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.dream-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dream-item h3 {
  color: #4b2e83;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.dream-item p {
  color: #666;
  line-height: 1.6;
}

.dream-item small {
  color: #999;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  display: block;
}

.dream-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  justify-content: flex-end;
}

.btn-edit {
  background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-edit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-danger {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

/* Modal Styles */
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
  padding: 2rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  color: #4b2e83;
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f0f0f0;
  color: #333;
}

/* Form Styles */
.dream-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4b2e83;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #4b2e83;
  box-shadow: 0 0 0 3px rgba(75, 46, 131, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.form-group small {
  color: #666;
  font-size: 0.8rem;
  margin-top: 0.25rem;
  display: block;
}

/* Checkbox Styles */
.checkbox-group {
  display: flex;
  flex-direction: column;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  margin-bottom: 0.5rem !important;
}

.checkbox-label input[type="checkbox"] {
  width: auto !important;
  margin-right: 0.5rem;
  margin-top: 0.1rem;
}

.checkbox-label span {
  flex: 1;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.btn-secondary {
  background: #f0f0f0;
  color: #666;
}

.btn-secondary:hover {
  background: #e0e0e0;
  transform: none;
  box-shadow: none;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Responsive */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 1rem;
  }
  
  .modal-content {
    max-height: 95vh;
  }
  
  .modal-header,
  .dream-form {
    padding: 1.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
