import React from 'react';
import { Box, Typography, Avatar, Paper, IconButton } from '@mui/material';
import { makeStyles } from '@material-ui/core/styles';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import PasteIcon from '@mui/icons-material/ContentPaste';

// Redux
import { connect } from 'react-redux';
import { create_element } from "../../../../actions"

const useStyles = makeStyles((theme) => ({
    commentContainer: {
        margin: theme.spacing(1),
        padding: theme.spacing(2),
        borderLeftWidth: 4, // Add a left border to indicate unread comments
        borderLeftColor: theme.palette.primary.main, // Customize the border color
        borderLeftStyle: (props) => (props.unread ? 'solid' : 'none'), // Show the border only for unread comments
    },
    commentAuthor: {
        fontWeight: 'bold',
        marginRight: theme.spacing(1),
    },
    commentDate: {
        fontSize: '0.8rem',
        color: theme.palette.text.secondary,
    },
    container: {
        position: 'relative',
    },
    buttonsContainer: {
        position: 'absolute',
        top: theme.spacing(1),
        right: theme.spacing(1),
        display: 'flex',
        alignItems: 'center',
    },
    button: {
        marginLeft: theme.spacing(1),
    },
}));

const Comment = ({ comment, unread, create_element, props }) => {
    const classes = useStyles({ unread: unread }); // Pass the unread status as a prop to useStyles

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

    const date = new Date(comment.date);
    const localTime = date.toLocaleString()

    return (
        <Box className={classes.container}>
            <div className={classes.buttonsContainer}>
                <IconButton className={classes.button} aria-label="Copy" onClick={handleCopy}>
                    <FileCopyIcon />
                </IconButton>
                <IconButton className={classes.button} aria-label="Paste" onClick={handlePaste}>
                    <PasteIcon />
                </IconButton>
            </div>
            <Paper className={classes.commentContainer} elevation={2}>
                <Box display="flex" alignItems="center" marginBottom={1}>
                    <Avatar alt={comment.author} style={{ marginRight: '8px' }}/>
                    <Typography variant="subtitle1" className={classes.commentAuthor}>
                        {comment.author}
                    </Typography>
                    <Typography variant="body1">{comment.body}</Typography>
                </Box>
                <Typography variant="caption" className={classes.commentDate}>
                    {localTime}
                </Typography>
            </Paper>
        </Box>
    );
};

export default connect(null, {
    create_element
})(Comment)
