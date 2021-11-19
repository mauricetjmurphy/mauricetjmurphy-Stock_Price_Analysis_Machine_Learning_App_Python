import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import fingerprint from "../images/fingerprint.svg";

const LoginFormContainer = styled.div`
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

const LoginFormImage = styled.img`
    width: 40px;
`;

function LoginForm() {
    return (
        <LoginFormContainer>
            <LoginFormImage src={fingerprint} />
            <input type="text" name="" id="" placeholder="Email" />
            <input type="password" name="" id="" placeholder="Password" />
            <button>Submit</button>
            <p>
                Not signed up yet?
                <Link to="/register">Register</Link>
            </p>
        </LoginFormContainer>
    );
}

export default LoginForm;
