import React, { useState } from 'react';
import { Box, Typography, Avatar, Paper, IconButton, TextareaAutosize } from '@mui/material';
import { styled } from '@mui/system';
import { FileCopy as FileCopyIcon, ContentPaste as PasteIcon, Edit as EditIcon, Save as SaveIcon, Cancel as CancelIcon } from '@mui/icons-material';

// Redux
import { connect } from 'react-redux';
import { create_element, create_answer } from "../../../../actions"

const StyledBox = styled(Box)(({ unread }) => ({
    borderLeft: unread ? '4px solid red' : 'none', // Show the border only for unread comments
}));

const Comment = ({ comment, unread, create_element, isnew, props, setIsAdding }) => {
    const [isEditing, setIsEditing] = useState(isnew);
    const [editedComment, setEditedComment] = useState(comment.body);

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
            comment.body,
            props.page_creator)
    };

    const handlePaste = () => {
        // Handle paste logic here
    };

    const handleEdit = () => {
        setIsEditing(true);
        setIsAdding(false)
    };

    const handleCancelEdit = () => {
        setIsEditing(false);
        setEditedComment(comment.body);
    };

    const handleSaveEdit = () => {
        // Save the answer
        props.create_answer(
            props.page_element.question[0].id,
            editedComment,
            props.page_creator)

        setIsEditing(false);
        setIsAdding(false)
    };

    const handleCommentChange = (event) => {
        setEditedComment(event.target.value);
    };

    const date = new Date(comment.date);
    const localTime = date.toLocaleString()

    return (
        <StyledBox margin={0.5} unread={unread}>
            <Paper elevation={2}>
                <Box display="flex" alignItems="center" padding={0.5}>
                    <Avatar alt={comment.author} style={{ marginRight: '8px' }} />
                    <Box flexGrow={1} marginRight={2}>
                        <Typography variant="subtitle1">
                            {comment.author}
                        </Typography>
                        {isEditing ? (
                            <TextareaAutosize
                                autoComplete="off"
                                name="text"
                                onChange={handleCommentChange}
                                autoFocus
                                className="text"
                                style={{ opacity: '1' }}
                                value={editedComment}
                            />
                        ) : (
                            <Typography variant="body1">{comment.body}</Typography>
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
                                <IconButton aria-label="Paste" onClick={handlePaste}>
                                    <PasteIcon />
                                </IconButton>
                            </>
                        )}
                    </Box>
                </Box>
                <Box margin={0.5}>
                    <Typography variant="caption">
                        {localTime}
                    </Typography>
                </Box>
            </Paper>
        </StyledBox>
    );
};

export default connect(null, {
    create_element,
    create_answer
})(Comment)
