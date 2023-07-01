//
// Reducer for questions and answers
//
export const questionsReducer = (questions = [], action) => {
    switch (action.type) {
        case "ADD_ANSWER":
            // Copy questions
            let question_array = [...questions]

            // Find the index of question
            let index = question_array.findIndex(x => x.id === action.payload.data.questionans)

            // Insert new answer at end of question
            question_array[index].answers.push(action.payload.data)
            return question_array;

        case "EDIT_ANSWER":
            // Copy questions
            question_array = [...questions]

            // Find the index of question
            index = question_array.findIndex(x => x.id === action.payload.data.questionans)

            // Find the index of answer
            let answer_index = question_array[index].answers.findIndex(x => x.id === action.payload.data.id);

            // update answer 
            question_array[index].answers[answer_index].body = action.payload.data.body;
            return question_array;

        case "SELECT_PAGE":
            // add all the questions of the page to redux store
            question_array = []

            if (action.payload === "page not found") {
                return question_array
            }

            action.payload.data.page_elements.forEach(element => {
                if (element.element_type === "Question") question_array.push(element.question[0])
            });
            return question_array

        default:
            return questions;
    }
};