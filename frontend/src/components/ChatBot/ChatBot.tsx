import { useState } from 'react';
import styles from './ChatBot.module.css';
import Loader from '../Loader/Loader';
import ChatMessages, { type Message } from '../ChatMessages/ChatMessages';
import ChatInput from '../ChatInput/ChatInput';
import { Assistant } from '../../assistants/assistant';


function ChatBot() {
    const assistant = new Assistant();
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [workflow_id, setWorkflowId] = useState<string | null>(null);

    function addMessage(message: Message) {
        setMessages((prevMessages) => [...prevMessages, message]);
    }

    async function handleMessageSend(content: string) {
        addMessage({role: "user", content: content});
        setIsLoading(true)
        try {
            const result = await assistant.chat(content, workflow_id);
            addMessage( { role: "assistant", content: result.response });
            setWorkflowId(result.workflow_id);

            if (result.status == 'clarification_required'){
                setWorkflowId(result.workflow_id);
            }
            else {
                setWorkflowId(null);
            }
        } catch (error){
            addMessage({
                role: "system",
                content: "Sorry, I couldn't process your request"
            });
            setWorkflowId(null);
        } finally {
            setIsLoading(false);
        }
    }
    return (
        <>
            {isLoading && <Loader />}
            <div className={styles.ChatBotContainer}>
                <ChatMessages messages={messages} />
            </div>
            <ChatInput isDisabled={isLoading} onSend={handleMessageSend} />
        </>
    )
}

export default ChatBot