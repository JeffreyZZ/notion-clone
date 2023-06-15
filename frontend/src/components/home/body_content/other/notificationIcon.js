import React from 'react';
import { Notifications } from '@material-ui/icons';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
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

const NotificationIcon = ({ count, onClick }) => {
  const classes = useStyles();

  return (
    <div className={classes.notificationIcon}>
      {count > 0 && <Notifications onClick={onClick}/>}
      {count > 0 && <div className={classes.notificationCount} onClick={onClick}>{count}</div>}
    </div>
  );
};

export default NotificationIcon;
