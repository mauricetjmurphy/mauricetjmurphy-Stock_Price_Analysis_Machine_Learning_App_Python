import React from "react";
import styled from "styled-components";
import backgroundImage from "../../images/loginbackground.jpg";
import LoginForm from "../../components/LoginForm";

const LoginContainer = styled.section`
    display: flex;
    width: 100vw;
    height: 100vh;
    background-image: url(${backgroundImage});
    background-position: center;
    background-size: cover;
    display: flex;
    align-items: center;
    justify-content: center;
`;

function LoginPage() {
    return (
        <LoginContainer>
            <LoginForm />
        </LoginContainer>
    );
}

export default LoginPage;
