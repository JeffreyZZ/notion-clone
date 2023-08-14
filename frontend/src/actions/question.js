import axios from 'axios';
import { getCookie } from './index'

// Configure axios to accept the CSRF Token
const headers = {
    'X-CSRFToken': getCookie('csrftoken')
}

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

// Add favorite to an Answer
export const add_answer_favorite = (answer_id, page_creator) =>
    async (dispatch) => {
        if (!headers.hasOwnProperty('Authorization')) {
            headers['Authorization'] = `Token ${localStorage.getItem('token')}`;
        }
        const response = await axios.patch(`/api_Answers/${answer_id}/add_favorite/`, {}, { headers: headers });
        dispatch({ type: 'ADD_ANSWER_FAVORITE', payload: response });
    }

// Remove favorite from an Answer
export const remove_answer_favorite = (answer_id, page_creator) =>
    async (dispatch) => {
        if (!headers.hasOwnProperty('Authorization')) {
            headers['Authorization'] = `Token ${localStorage.getItem('token')}`;
        }
        const response = await axios.patch(`/api_Answers/${answer_id}/remove_favorite/`, {}, { headers: headers });
        dispatch({ type: 'REMOVE_ANSWER_FAVORITE', payload: response });
    }