import React, { useState } from 'react';
import { Box, Typography, Avatar, Paper, IconButton, TextareaAutosize } from '@mui/material';
import { styled } from '@mui/system';
import { FileCopy as FileCopyIcon, Edit as EditIcon, Save as SaveIcon, Cancel as CancelIcon } from '@mui/icons-material';

// Redux
import { connect } from 'react-redux';
import { create_element, add_answer, edit_answer } from "../../../../actions"

const StyledBox = styled(Box)(({ unread }) => ({
    borderLeft: unread ? '4px solid red' : 'none', // Show the border only for unread answers
}));

const Answer = ({ answer, unread, create_element, isnew, props, setIsAdding }) => {
    const [isEditing, setIsEditing] = useState(isnew);
    const [editedAnswer, setEditedAnswer] = useState(answer.body);

    // copy the answer content and create a text component 
    const handleCopy = () => {
        // Find the order of the element after the current element
        let element_above_order = null
        if (props.page_element_index !== (props.column_elements.length - 1)) {
            if (props.page_element_index === -1) {
                element_above_order = 0
            } else {
                element_above_order = props.column_elements[props.page_element_index + 1].order_on_page
            }
        }

        // Handle copy logic here
        create_element(
            props.page_element_index,
            props.page_element.id,
            "Text",
            props.page_element.order_on_page,
            element_above_order,
            undefined,
            answer.body,
            props.page_creator)
    };

    const handleEdit = () => {
        setIsEditing(true);
        setIsAdding(false)
    };

    const handleCancelEdit = () => {
        setIsEditing(false);
        setEditedAnswer(answer.body);
    };

    const handleSaveEdit = () => {
        if (isnew) {
            props.add_answer(
                props.page_element.question[0].id,
                editedAnswer,
                props.page_creator)
        }
        else {
            props.edit_answer(
                answer.id,
                editedAnswer)
        }

        setIsEditing(false);
        setIsAdding(false)
    };

    const handleAnswerChange = (event) => {
        setEditedAnswer(event.target.value);
    };

    const date = answer.date ? new Date(answer.date) : new Date();
    const localTime = date.toLocaleString();

    return (
        <StyledBox margin={0.5} unread={unread}>
            <Paper elevation={2}>
                <Box display="flex" alignItems="center" padding={0.5}>
                    <Avatar alt={answer.author} style={{ marginRight: '8px' }} />
                    <Box flexGrow={1} marginRight={2}>
                        <Typography variant="author">
                            {answer.author}
                        </Typography>
                        {isEditing ? (
                            <TextareaAutosize
                                autoComplete="off"
                                name="text"
                                onChange={handleAnswerChange}
                                autoFocus
                                className="text"
                                style={{ opacity: '1' }}
                                value={editedAnswer}
                            />
                        ) : (
                            <Typography variant="body1">{answer.body}</Typography>
                        )}
                    </Box>
                    <Box>
                        {!isEditing && (
                            <IconButton aria-label="Edit" onClick={handleEdit}>
                                <EditIcon />
                            </IconButton>
                        )}
                        {isEditing ? (
                            <>
                                <IconButton aria-label="Save" onClick={handleSaveEdit}>
                                    <SaveIcon />
                                </IconButton>
                                <IconButton aria-label="Cancel" onClick={handleCancelEdit}>
                                    <CancelIcon />
                                </IconButton>
                            </>
                        ) : (
                            <>
                                <IconButton aria-label="Copy" onClick={handleCopy}>
                                    <FileCopyIcon />
                                </IconButton>
                            </>
                        )}
                    </Box>
                </Box>
                <Box margin={0.5}>
                    <Typography variant="time">
                        {localTime}
                    </Typography>
                </Box>
            </Paper>
        </StyledBox>
    );
};

export default connect(null, {
    create_element,
    add_answer,
    edit_answer
})(Answer)
