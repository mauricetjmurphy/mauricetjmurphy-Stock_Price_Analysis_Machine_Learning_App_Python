import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import fingerprint from "../images/fingerprint.svg";

const RegisterFormContainer = styled.div`
    background: #fff;
    width: 450px;
    height: 500px;
    opacity: 90%;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
`;

const RegisterFormImage = styled.img`
    width: 40px;
`;

function RegisterForm() {
    return (
        <RegisterFormContainer>
            <RegisterFormImage src={fingerprint} />
            <input type="text" name="" id="" placeholder="Full Name" />
            <input type="text" name="" id="" placeholder="Email" />
            <input type="password" name="" id="" placeholder="Password" />
            <button>Submit</button>
            <p>
                Already signed up?
                <Link to="/">Login</Link>
            </p>
        </RegisterFormContainer>
    );
}

export default RegisterForm;
