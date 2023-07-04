import React, { useState, useRef, useEffect } from "react";
import { connect } from 'react-redux';
import { change_tickBox, change_description } from "../../../../actions/to_do"
import CheckIcon from '@material-ui/icons/Check';

function To_do(props) {
    const myRef = useRef();

    useEffect(() => {
        myRef.current.focus({ preventScroll: true });
    }, [])

    // In case there is an element whose type is to-do but there is no to-do...
    if ((props.page_element.to_do).length === 0) return null

    const to_do = props.page_element.to_do[0]

    // State
    const [initialDescription, setInitialDescription] = useState(to_do.description)
    const [description, set_description] = useState(to_do.description)
    const [complete, change_complete] = useState(to_do.completed)

    // Toggle check box
    const toggleCheckBox = () => {
        const newComplete = !complete;
        change_complete(newComplete)
        change_tickBox(newComplete, to_do.id)
    }

    const handleBlur = () => {
        if (description !== initialDescription) {
            change_description(description, to_do.id)
            setInitialDescription(description)
        }
    }

    return (
        <div className={`to-do ${props.page_element.color}`}
            style={{ opacity: props.snapshot.isDragging ? '0.5' : '1' }}>

            {/* Checkbox */}
            <div className="checkbox">

                {/* Checkbox empty */}
                <input type='checkbox' checked={complete} onChange={toggleCheckBox} />

                {/* Checkbox checked */}
                {complete === true ?
                    <span className="to-do-check" onClick={toggleCheckBox}>
                        <CheckIcon fontSize="inherit" />
                    </span> : null}
            </div>

            {/* To-do text */}
            <input
                ref={myRef}
                type="text"
                onChange={(e) => set_description(e.target.value)}
                onBlur={handleBlur}
                value={description ? description : ""}
                placeholder="To-do" className={complete === false ? "user_input" : "user_input completed"}
                onKeyDown={(e) => { if (e.key === 'Enter') e.target.blur(); }} />
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        selected_page: state.selected_page
    }
}

export default connect(mapStateToProps, {
    change_tickBox,
    change_description
})(To_do);