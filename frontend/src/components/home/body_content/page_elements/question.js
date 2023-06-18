import React, { useState } from "react";
import TextareaAutosize from 'react-textarea-autosize';
import QuestionIcon from '@mui/icons-material/HelpOutline';
import NotificationIcon from '../other/notificationIcon';
import { Collapse } from '@material-ui/core';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import QuestionComment from './comment';

function Question(props) {

    // In case there is an element whose type is text but there is no text...
    if ((props.page_element.question).length === 0) return null

    const [body, set_body] = useState(props.page_element.question[0].body)
    const [title, set_title] = useState(props.page_element.question[0].title)

    const [open, setOpen] = useState(false);

    const handleClick = () => {
        setOpen(!open);
    };

    return (
        <div className={`text-element ${props.page_element.color}`}>
            <div className={`to-do ${props.page_element.color}`}>
                {/* Render the question mark icon */}
                <QuestionIcon
                    className="Question_icon"
                    style={{ opacity: props.snapshot.isDragging ? '0.5' : '1', height: '32px' }} />

                <TextareaAutosize
                    autoComplete="off"
                    name="text"
                    onChange={(e) => set_title(e.target.value)} value={title}
                    placeholder="Type your question title here..."
                    autoFocus
                    className="text"
                    onBlur={() => props.edit_question(props.page_element.question[0].id, title, body)}
                    style={{ opacity: props.snapshot.isDragging ? '0.5' : '1' }} />

                <NotificationIcon
                    count={props.page_element.question[0].notification.length}
                    onClick={handleClick} />
            </div>

            <TextareaAutosize
                autoComplete="off"
                name="text"
                onChange={(e) => set_body(e.target.value)} value={body}
                placeholder="Type your question details here..."
                autoFocus
                className="text"
                onBlur={() => props.edit_question(props.page_element.question[0].id, title, body)}
                style={{ opacity: props.snapshot.isDragging ? '0.5' : '1' }} />

            {/* Render the question's answers */}
            <div>
                <Collapse in={open}>
                    <div>
                        <AppBar position="static">
                            <Toolbar>
                                <IconButton
                                    size="small"
                                    edge="start"
                                    color="inherit"
                                    aria-label="menu"
                                    sx={{ mr: 1 }}
                                >
                                    <QuestionAnswerIcon />
                                </IconButton>
                                <Typography variant="h8" component="div" sx={{ flexGrow: 1 }}>
                                    Answers
                                </Typography>
                                <Button color="inherit">Details</Button>
                            </Toolbar>
                        </AppBar>

                        <ul style={{ listStyleType: 'none', padding: 0 }}>
                            {props.page_element.question[0].answers.map((answer, index) => {
                                const unread = props.page_element.question[0].notification.some(
                                    (notification) => notification.answer_noti === answer.id
                                );
                                return <QuestionComment comment={answer} unread={unread} props={props}/>
                            })}
                        </ul>
                    </div>
                </Collapse>
            </div>
        </div>
    )
}
export default Question