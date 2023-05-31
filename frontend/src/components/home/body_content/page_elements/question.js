import React, { useState } from "react";
import TextareaAutosize from 'react-textarea-autosize';
import QuestionIcon from '@mui/icons-material/HelpOutline';

function Question(props) {

    // In case there is an element whose type is text but there is no text...
    if ((props.page_element.question).length === 0) return null
    
    const [body, set_body] = useState(props.page_element.question[0].body)
    const [title, set_title] = useState(props.page_element.question[0].title)

    return (
        <div className={`text-element ${props.page_element.color}`}>
            <div className={`to-do ${props.page_element.color}`}> 
                {/* Render the question mark icon */}
                <QuestionIcon 
                    className="Question_icon" 
                    style={{ opacity: props.snapshot.isDragging ? '0.5' : '1', height: '32px'}} />

                <TextareaAutosize
                    autoComplete="off"
                    name="text"
                    onChange={(e) => set_title(e.target.value)} value={title}
                    placeholder="Type your question title here..."
                    autoFocus
                    className="text"
                    onBlur={() => props.edit_question(props.page_element.question[0].id, title, body)}
                    style={{ opacity: props.snapshot.isDragging ? '0.5' : '1' }} />
            </div>

            <TextareaAutosize 
                autoComplete="off" 
                name="text" 
                onChange={(e) => set_body(e.target.value)} value={body} 
                placeholder="Type your question details here..." 
                autoFocus 
                className="text"
                onBlur={()=> props.edit_question(props.page_element.question[0].id, title, body)} 
                style={{ opacity: props.snapshot.isDragging? '0.5': '1' }} />
        </div>
    )
}
export default Question