import React from "react";
import styled from "styled-components";

const FooterContainer = styled.section`
    height: 40px;
    width: 100vw;
    background: #202020;
    color: #fff;
    position: fixed;
    bottom: 0;

    p {
        line-height: 40px;
        margin: 0;
        text-align: center;
    }
`;

function Footer() {
    return (
        <FooterContainer>
            <p>Copyright &copy; Maurice Murphy 2021</p>
        </FooterContainer>
    );
}

export default Footer;
