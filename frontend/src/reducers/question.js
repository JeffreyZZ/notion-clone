//
// Reducer for questions and answers
//
export const questionsReducer = (questions = [], action) => {
    switch (action.type) {
        case "ADD_ANSWER":
            // Copy questions
            let question_array = [...questions]

            // Find all the questions and add answer
            question_array.forEach((question, index) => {
                if (question.id === action.payload.data.questionans) {
                    question_array[index].answers.push(action.payload.data);
                }
            });

            return question_array;

        case "DELETE_ANSWER":
            // Copy questions
            question_array = [...questions]

            // Find all the questions and remove answer
            question_array.forEach((question, index) => {
                if (question.id === action.payload.question_id) {
                    question_array[index].answers = question_array[index].answers.filter(x => x.id !== action.payload.answer_id);
                }
            });

            return question_array;

        case "EDIT_ANSWER":
            // Copy questions
            question_array = [...questions]

            // Find all the questions and update answer
            question_array.forEach((question, index) => {
                if (question.id === action.payload.data.questionans) {
                    // Find the index of answer and update answer
                    let answer_index = question_array[index].answers.findIndex(x => x.id === action.payload.data.id);
                    question_array[index].answers[answer_index].body = action.payload.data.body;
                }
            });

            return question_array;

        case "SELECT_PAGE":
            // add all the questions of the page to redux store
            question_array = []

            if (action.payload === "page not found") {
                return question_array
            }

            action.payload.data.page_elements.forEach(element => {
                if (element.element_type === "Question") question_array.push(element.question)
            });
            return question_array

        case "REMOVE_QUESTION_TAG":
            // Copy questions
            question_array = [...questions]

            // Find the question and remove the tag
            question_array.forEach((question, index) => {
                if (question.id === action.payload.data.id) {
                    question_array[index].tags = action.payload.data.tags;
                    return;
                }
            });
            return question_array;

        case "ADD_QUESTION_TAG":
            // Copy questions
            question_array = [...questions]

            // Find the question and add the tag
            question_array.forEach((question, index) => {
                if (question.id === action.payload.data.id) {
                    question_array[index].tags = action.payload.data.tags;
                    return;
                }
            });
            return question_array;

        default:
            return questions;
    }
};