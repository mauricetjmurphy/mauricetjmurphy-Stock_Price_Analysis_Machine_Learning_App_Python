import React from "react";
import styled from "styled-components";

const SentimentFormContainer = styled.form`
    display: flex;
    flex-direction: column;
    text-align: left;

    h1 {
        margin: 15px 0;
    }

    label {
        margin-bottom: 10px;
        font-size: 12px;
    }

    input[type="date"] {
        margin-bottom: 10px;
    }
`;

function SentimentForm() {
    return (
        <SentimentFormContainer>
            <h1 htmlFor="">Select a stock</h1>
            <select name="" id=""></select>

            <button>Submit</button>
        </SentimentFormContainer>
    );
}

export default SentimentForm;
