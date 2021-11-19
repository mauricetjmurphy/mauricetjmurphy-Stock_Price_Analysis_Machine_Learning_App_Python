import React from "react";
import styled from "styled-components";
import RegisterForm from "../../components/RegisterForm";
import backgroundImage from "../../images/loginbackground.jpg";

const RegisterContainer = styled.section`
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

function RegisterPage() {
    return (
        <RegisterContainer>
            <RegisterForm />
        </RegisterContainer>
    );
}

export default RegisterPage;
