import React from 'react';
import { Box, Badge, IconButton } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { styled } from '@mui/system';

const useStyles = styled({
  notificationIcon: {
    position: 'relative',
    display: 'inline-block',
  },
  notificationCount: {
    position: 'absolute',
    top: -2,
    right: -2,
    backgroundColor: 'red',
    color: 'white',
    borderRadius: '50%',
    width: 16,
    height: 16,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontSize: 10,
    fontWeight: 'bold',
  },
});

const StyledBadge = styled(Badge)(({ theme }) => ({
  '& .MuiBadge-badge': {
    fontSize: 10,
    backgroundColor: 'red',
    color: 'white',
  },
}));

const NotificationIcon = ({ count, onClick }) => {
  const classes = useStyles();

  return (
    <Box position="relative">
      <IconButton onClick={onClick}>
        <StyledBadge badgeContent={count}>
          <NotificationsIcon />
        </StyledBadge>
      </IconButton>
    </Box>
  );
};

export default NotificationIcon;
