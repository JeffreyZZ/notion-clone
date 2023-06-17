import React from 'react';
import { Box, Typography, Avatar, Paper } from '@mui/material';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    commentContainer: {
        margin: theme.spacing(2),
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
}));

const Comment = ({ comment, unread }) => {
    const classes = useStyles({ unread: unread }); // Pass the unread status as a prop to useStyles

    return (
        <Paper className={classes.commentContainer} elevation={2}>
            <Box display="flex" alignItems="center" marginBottom={1}>
                <Avatar alt={comment.author} />
                <Typography variant="subtitle1" className={classes.commentAuthor}>
                    {comment.author}
                </Typography>
                <Typography variant="caption" className={classes.commentDate}>
                    {comment.date}
                </Typography>
            </Box>
            <Typography variant="body1">{comment.body}</Typography>
        </Paper>
    );
};

export default Comment;
