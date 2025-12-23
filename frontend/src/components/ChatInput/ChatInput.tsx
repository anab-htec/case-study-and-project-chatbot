import { useEffect, useRef, useState } from 'react';
import TextareaAutosize from 'react-textarea-autosize';
import styles from './ChatInput.module.css';

interface ChatInputProps {
    isDisabled: boolean;
    onSend: (message: string) => void;
}
function ChatInput({ isDisabled, onSend }: ChatInputProps) {
    const [message, setMessage] = useState('');
    const textAreaRef = useRef<HTMLTextAreaElement | null>(null)

    useEffect(() => {
        textAreaRef.current?.focus();
    }, [isDisabled])

    function handleMessageChange(event: React.ChangeEvent<HTMLTextAreaElement>) {
        setMessage(event.target.value)
    }

    function handleMessageSend() {
        if (message.length > 0){
            onSend(message);
            setMessage('');
        }
    }

    function handleEnterPress(event: React.KeyboardEvent<HTMLTextAreaElement>) {
         if (event.key === "Enter" && !event.shiftKey){
            event.preventDefault();
            handleMessageSend();
        }
    }
    
    return (
        <div className={styles.ChatInput}>
            <div className={styles.TextAreaContainer}>
                <TextareaAutosize 
                    ref={textAreaRef}
                    className={styles.TextArea}
                    disabled={isDisabled}
                    minRows={1}
                    maxRows={4}
                    value={message}
                    placeholder="Ask Chatbot"
                    onChange={handleMessageChange}
                    onKeyDown={handleEnterPress} />
            </div>
            <button 
                className={styles.Button}
                disabled={isDisabled}
                onClick={handleMessageSend}>
                <SendIcon />
            </button>
        </div>
    )
}

function SendIcon() {
    return (
        <svg 
        xmlns="http://www.w3.org/2000/svg" 
        height="24px" 
        viewBox="0 -960 960 960" 
        width="24px" 
        fill="#FFFFFF">
            <path d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"/>
        </svg>
    )
}

export default ChatInput