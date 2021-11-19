import React from "react";
import styled from "styled-components";

const StockFormContainer = styled.form`
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

function StockForm() {
    return (
        <StockFormContainer>
            <h1 htmlFor="">Select a stock</h1>
            <select name="" id=""></select>
            <h1 htmlFor="">Select a date range</h1>
            <label htmlFor="">From</label>
            <input type="date" name="" id="" />
            <label htmlFor="">To</label>
            <input type="date" name="" id="" />
            <button>Submit</button>
        </StockFormContainer>
    );
}

export default StockForm;
