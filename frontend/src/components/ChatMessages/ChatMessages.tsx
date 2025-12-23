import Markdown from 'react-markdown';
import styles from './ChatMessages.module.css'
import { useEffect, useMemo, useRef } from 'react';

export interface Message {
    role: string;
    content: string;
}

interface ChatMessagesProps {
    messages: Message []
}

const WELCOME_MESSAGE = [
  {
    role: "assistant",
    content: "Hello! I’m your **Project & Case Study Intelligence Assistant**. I can help you find **specific project matches** based on technology stacks or retrieve **relevant case studies** to support your proposals. What are you looking for today?",
  },
];

function ChatMessages({messages}: ChatMessagesProps) {
    const messagesEndRef = useRef<HTMLDivElement | null>(null);
    const messagesGroups = useMemo(
        () =>
        messages.reduce<Message[][]>((groups, message) => {
            if (message.role === "user") groups.push([]);
            groups[groups.length - 1].push(message);
            return groups;
        }, []),
        [messages]
    );

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <div className={styles.ChatMessagesContainer}>
            {[WELCOME_MESSAGE, ...messagesGroups].map((messages, groupIndex) => (
                <div key={groupIndex} className={styles.Group}>
                    {messages.map(({role, content}, index) => (
                        <div key={index} className={styles.Message} data-role={role}>
                             <Markdown>{content}</Markdown>
                        </div>
                    ))}
                </div>    
            ))}
            <div ref={messagesEndRef} />
        </div>      
    )
}

export default ChatMessages