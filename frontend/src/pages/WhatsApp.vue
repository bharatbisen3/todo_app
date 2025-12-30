<template>
  <div class="whatsapp-container">
    <div class="whatsapp-sidebar">
      <h3>Contacts</h3>
      <div class="contact-list">
        <div 
          v-for="contact in contacts" 
          :key="contact.name"
          @click="selectContact(contact)"
          :class="{'active': selectedContact?.name === contact.name}"
          class="contact-item"
        >
          <div class="contact-info">
            <h4>{{ contact.contact_name }}</h4>
            <p>{{ contact.phone_number }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-area">
      <div v-if="selectedContact" class="chat-container">
        <div class="chat-header">
          <h3>{{ selectedContact.contact_name }}</h3>
          <span>{{ selectedContact.phone_number }}</span>
        </div>

        <div class="messages-container" ref="messageContainer">
          <div 
            v-for="message in messages" 
            :key="message.name"
            :class="['message', message.message_type.toLowerCase()]"
          >
            <div class="message-content">
              <p>{{ message.message }}</p>
              <span class="time">{{ formatTime(message.timestamp) }}</span>
            </div>
          </div>
        </div>

        <div class="message-input">
          <input 
            v-model="newMessage"
            @keyup.enter="sendMessage"
            type="text" 
            placeholder="Type a message..."
          />
          <button @click="sendMessage">
            <i class="fa fa-paper-plane"></i>
          </button>
        </div>
      </div>

      <div v-else class="no-chat-selected">
        <i class="fa fa-whatsapp"></i>
        <p>Select a contact to start chatting</p>
      </div>
    </div>
  </div>
</template>

<script>
import { createResource } from 'frappe-ui'

export default {
  name: 'WhatsApp',
  data() {
    return {
      contacts: [],
      messages: [],
      selectedContact: null,
      newMessage: ''
    }
  },
  mounted() {
    this.loadContacts()
    this.setupRealtimeUpdates()
  },
  methods: {
    loadContacts() {
      this.$call('todo_app.api.whatsapp.get_contacts').then(r => {
        this.contacts = r.message
      })
    },
    
    selectContact(contact) {
      this.selectedContact = contact
      this.loadMessages(contact.name)
    },
    
    loadMessages(contactName) {
      this.$call('todo_app.api.whatsapp.get_messages', {
        contact: contactName
      }).then(r => {
        this.messages = r.message
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      })
    },
    
    sendMessage() {
      if (!this.newMessage.trim()) return
      
      this.$call('todo_app.api.whatsapp.send_message', {
        contact: this.selectedContact.name,
        message: this.newMessage
      }).then(r => {
        this.messages.push(r.message)
        this.newMessage = ''
        this.scrollToBottom()
      })
    },
    
    setupRealtimeUpdates() {
      frappe.realtime.on('whatsapp_message', (data) => {
        if (this.selectedContact?.name === data.contact) {
          this.messages.push(data.message)
          this.scrollToBottom()
        }
        this.loadContacts() // Update last message
      })
    },
    
    scrollToBottom() {
      const container = this.$refs.messageContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.whatsapp-container {
  display: flex;
  height: calc(100vh - 60px);
  background: #f0f2f5;
}

.whatsapp-sidebar {
  width: 350px;
  background: white;
  border-right: 1px solid #e0e0e0;
}

.contact-list {
  overflow-y: auto;
  height: calc(100% - 60px);
}

.contact-item {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.contact-item:hover,
.contact-item.active {
  background: #f5f5f5;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #e5ddd5;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  background: white;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 10px;
  display: flex;
}

.message.sent {
  justify-content: flex-end;
}

.message.received {
  justify-content: flex-start;
}

.message-content {
  background: white;
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 60%;
}

.message.sent .message-content {
  background: #dcf8c6;
}

.message-input {
  background: white;
  padding: 15px;
  display: flex;
  gap: 10px;
}

.message-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
}

.message-input button {
  padding: 10px 20px;
  background: #25d366;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
}

.no-chat-selected {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #999;
}
</style>