import React, { useState } from "react";
import { TextareaAutosize } from '@mui/material';

function Text(props) {

    // In case there is an element whose type is text but there is no text...
    if ((props.page_element.text).length === 0) return null

    const initialValue = props.page_element.text[0].text;
    const [text, set_text] = useState(initialValue)

    const handleBlur = () => {
        if (text !== initialValue) {
            props.edit_text(props.page_element.text[0].id, text);
        }
    };

    const handleChange = (e) => {
        set_text(e.target.value);
    };

    return (
        <div className={`text-element ${props.page_element.color}`}>
            <TextareaAutosize
                autoComplete="off"
                name="text"
                value={text}
                onChange={handleChange}
                placeholder="Type your text here..."
                className="text"
                onBlur={handleBlur}
                style={{ opacity: props.snapshot.isDragging ? '0.5' : '1' }} />
        </div>
    )
}

export default Text