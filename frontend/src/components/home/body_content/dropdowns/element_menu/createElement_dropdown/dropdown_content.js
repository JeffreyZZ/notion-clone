import React, { useState } from "react";
import ListOfPages from "./listOfPages";
import DropdownOption from "./dropdown_option";
import Button from '@mui/material/Button';
import CancelIcon from '@mui/icons-material/Cancel';
import SendIcon from '@mui/icons-material/Send';

// Redux
import { connect } from 'react-redux';
import { create_element } from "../../../../../../actions"

// Dropdown photos
import text from "./dropdown_icons/text.png";
import question from "./dropdown_icons/question.png";
import to_do from "./dropdown_icons/to-do.png"; 
import heading_1 from "./dropdown_icons/heading_1.png";
import heading_2 from "./dropdown_icons/heading_2.png";
import link_to_page from "./dropdown_icons/link-to-page.png";
import table from "./dropdown_icons/table.png";
import board from "./dropdown_icons/board.png";

const CreateElement_dropdownContent = (props) => {
    const [listOfPage_open, setListOfPage_open] = useState(false);
    const [questionIdInputShown, setQuestionIdInputShown] = useState(false);
    const [questionId, setQuestionId] = useState("");

    // Function for when a user clicks to create a new item
    const create_element_func = async (element_type, element_above_order, sub_element_type) => {
        props.create_element(props.index, props.page.id, element_type, props.order_on_page, element_above_order, undefined, "...", props.page.creator, sub_element_type, undefined);
        props.setDropdownShown(false);
    }

    const showQuestionIdInputDialog = async () => {
        setQuestionIdInputShown(true);
    }

    // Find the order of the element after the current element
    let element_above_order = null

    if (props.index !== (props.column_elements.length - 1)) {
        if (props.index === -1) {
            element_above_order = 0
        } else {
            element_above_order = props.column_elements[props.index + 1].order_on_page
        }
    }

    const handleInputChange = (event) => {
        setQuestionId(event.target.value);
    }

    const handleCancel = (event) => {
        setQuestionIdInputShown(false);
        props.setDropdownShown(false);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        setQuestionIdInputShown(false);
        props.setDropdownShown(false);
        props.create_element(props.index, props.page.id, "Question", props.order_on_page, element_above_order, undefined, "...", props.page.creator, "Existing", questionId);
    }

    const centeredFormStyle = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
    };

    const inputContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
    };

    const inputStyle = {
        width: '250px', // Adjust the width as per your requirement
        padding: '8px', // Adjust the padding as needed
    };

    const buttonRowStyle = {
        display: 'flex',
        justifyContent: 'center',
        marginTop: '10px',
    };

    if (!listOfPage_open)
        return (
            <div className="dropdown-content add-element-drpdn">
                {/* Text */}
                <DropdownOption
                    create_element_func={create_element_func}
                    elementType="Text"
                    element_above_order={element_above_order}
                    photo={text}
                    header="Text"
                    subheader="Just start writing with plain text."
                />

                {/* Question */}
                <DropdownOption
                    create_element_func={create_element_func}
                    elementType="Question"
                    element_above_order={element_above_order}
                    photo={question}
                    header="Question"
                    subheader="Ask a new question."
                />

                {/* Question */}
                <DropdownOption
                    create_element_func={showQuestionIdInputDialog}
                    elementType="Question"
                    sub_elementType="Existing"
                    element_above_order={element_above_order}
                    photo={question}
                    header="Question"
                    subheader="Reference an existing question."
                />

                {/* To do */}
                <DropdownOption
                    create_element_func={create_element_func}
                    elementType="To_do"
                    element_above_order={element_above_order}
                    photo={to_do}
                    header="To-do list"
                    subheader="Track tasks with a to-do list."
                />

                {/* Heading 1 */}
                <DropdownOption
                    create_element_func={create_element_func}
                    elementType="Heading_1"
                    element_above_order={element_above_order}
                    photo={heading_1}
                    header="Heading 1"
                    subheader="Big section heading."
                />

                {/* Heading 2 */}
                <DropdownOption
                    create_element_func={create_element_func}
                    elementType="Heading_2"
                    element_above_order={element_above_order}
                    photo={heading_2}
                    header="Heading 2"
                    subheader="Sub-section heading."
                />

                {/* Link to page */}
                <div onClick={() => setListOfPage_open(true)}>
                    <a>
                        <img className="drpdn-icon" src={link_to_page} alt="Link to page" />
                        <div className="drpdn-text">
                            <p className="drpdn-head">Link to page</p>
                            <p className="drpdn-sub-head">Link to an existing page.</p>
                        </div>
                    </a>
                </div>

                {/* Table */}
                <DropdownOption
                    create_element_func={create_element_func}
                    elementType="Table"
                    element_above_order={element_above_order}
                    photo={table}
                    header="Table"
                    subheader="Create a table."
                />

                {/* Kanban */}
                <DropdownOption
                    create_element_func={create_element_func}
                    elementType="Kanban"
                    element_above_order={element_above_order}
                    photo={board}
                    header="Board"
                    subheader="Create a kanban board."
                />

                {/* Question Id Input Dialog */}
                {questionIdInputShown &&
                    <div style={centeredFormStyle}>
                        <div className="semi-transparent-bg">
                            <div className="modal">
                                <form onSubmit={handleSubmit}>
                                    <div style={inputContainerStyle}>
                                        <label>
                                            Enter the question id:
                                            <input type="number" value={questionId} onChange={handleInputChange} style={inputStyle}/>
                                        </label>
                                        <div style={buttonRowStyle}>
                                            <Button
                                                type="submit"
                                                variant="contained"
                                                style={{ color: 'black', marginRight: '8px' }}
                                            >
                                                Submit
                                            </Button>
                                            <Button
                                                type="button"
                                                variant="contained"
                                                style={{ color: 'black' }}
                                                onClick={handleCancel}
                                            >
                                                Cancel
                                            </Button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>}
            </div>    
        )
    return (
        <ListOfPages
                create_element={props.create_element}
                index={props.index}
                page={props.page}
                order_on_page={props.order_on_page}
                element_above_order={element_above_order}
                element={props.element}
                setDropdownShown={props.setDropdownShown} /> 
    )
};
export default connect(null, {
    create_element
})(CreateElement_dropdownContent)