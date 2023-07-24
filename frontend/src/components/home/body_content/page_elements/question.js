// General React and Redux
import React, { useState } from "react";
import { connect } from 'react-redux';
import { add_answer, delete_answer, edit_answer, remove_question_tag, add_question_tag } from './../../../../actions'

import { AppBar, Button, Collapse, Typography, IconButton, TextareaAutosize, Toolbar, Chip, Stack } from '@mui/material';
import NotificationIcon from '../other/notificationIcon';;
import QuestionIcon from '@mui/icons-material/HelpOutline';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import QuestionAnswer from './answer';

function Question(props) {

    // In case there is an element whose type is text but there is no text...
    if (props.page_element.question === null || props.page_element.question.id === undefined ) return null

    const [body, set_body] = useState(props.page_element.question.body)
    const [title, set_title] = useState(props.page_element.question.title)

    const [initialValues, setInitialValues] = useState({
        title: props.page_element.question.title,
        body: props.page_element.question.body,
    });

    const [newTag, setNewTag] = useState("");

    const handleBlur = () => {
        if (title !== initialValues.title || body !== initialValues.body) {
            props.edit_question(props.page_element.question.id, title, body);
            setInitialValues({ title, body });
        }
    };

    const [open, setOpen] = useState(false);

    const handleClick = () => {
        setOpen(!open);
    };

    const [isAdding, setIsAdding] = useState(false);
    const handleAddAnswer = () => {
        setIsAdding(true)
    };

    // Function to remove an existing tag
    const handleRemoveTag = (tagToRemove) => {
        props.remove_question_tag(props.page_element.question.id, tagToRemove);
    };

    const handleAddTag = () => {
        if (newTag.trim() !== "") {
            props.add_question_tag(props.page_element.question.id, newTag.trim());
            setNewTag("");
        }
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
                    value={title}
                    onChange={(e) => set_title(e.target.value)}
                    placeholder="Type your question title here..."
                    className="text"
                    onBlur={handleBlur}
                    style={{ opacity: props.snapshot.isDragging ? '0.5' : '1' }} />

                <NotificationIcon
                    count={props.page_element.question.notification.length}
                    onClick={handleClick} />
            </div>

            {/* Render the question's tags */}
            <div style={{ display: "flex", alignItems: "center" }}>
                <Stack direction="row" spacing={1}>
                    {props.page_element.question.tags.map((tag) => (
                        <Chip key={tag} label={tag} color="primary" variant="outlined" size="small" onDelete={() => handleRemoveTag(tag)} />
                    ))}

                    <input
                        type="text"
                        value={newTag}
                        onChange={(e) => setNewTag(e.target.value)}
                        placeholder="Add a new tag"
                        style={{ marginBottom: "8px", marginRight: "8px" }}
                    />
                    <Button variant="contained" color="primary" size="small" style={{ textTransform: "none" }} onClick={handleAddTag} >
                        Add Tag
                    </Button>
                </Stack>
            </div>

            <TextareaAutosize
                autoComplete="off"
                name="text"
                value={body}
                onChange={(e) => set_body(e.target.value)}
                placeholder="Type your question details here..."
                className="text"
                onBlur={handleBlur}
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
                                <Button color="inherit" onClick={handleAddAnswer}>Add</Button>
                            </Toolbar>
                        </AppBar>

                        <ul style={{ listStyleType: 'none', padding: 0 }}>
                            {props.page_element.question.answers.map((answer, index) => {
                                const unread = props.page_element.question.notification.some(
                                    (notification) => notification.answer_noti === answer.id
                                );
                                return <QuestionAnswer answer={answer} unread={unread} props={props} />
                            })}

                            {isAdding && (
                                <QuestionAnswer answer={""} unread={false} props={props} isnew={isAdding} setIsAdding={setIsAdding} />
                            )}
                        </ul>
                    </div>
                </Collapse>
            </div>
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        questions: state.questions,
        // connect Question component with selected_page in Redux store
        // UI get re-rendered when selected_page is updated, such as color change.
        selected_page: state.selected_page,
    }
}

export default connect(mapStateToProps, {
    add_answer,
    delete_answer,
    edit_answer,
    remove_question_tag,
    add_question_tag,
})(Question)