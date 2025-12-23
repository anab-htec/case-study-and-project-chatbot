import styles from './App.module.css';
import ChatBot from './components/ChatBot/ChatBot';

function App() {
  return (
     <div className={styles.App}>
      <header className={styles.Header}>
        <img className={styles.Logo} src="/chat-bot.png" />
        <h2 className={styles.Title}>HTEC Project and Case Study Chatbot</h2>
      </header> 
      <ChatBot />
    </div>
  )
}

export default App
