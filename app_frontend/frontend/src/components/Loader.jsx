import React from "react";
import styled from "styled-components";
import LoaderGif from "../images/loader.gif";

const LoaderContainer = styled.div`
    flex: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
`;

const LoaderImage = styled.img`
    width: 50%;
`;

function Loader() {
    return (
        <LoaderContainer>
            <p>
                Fetching Twitter data and processing the model. This can take up
                to 5 minutes depending on your internet connection and the power
                of your CPU.
            </p>
            <LoaderImage src={LoaderGif}></LoaderImage>
            <h1>Processing...</h1>
        </LoaderContainer>
    );
}

export default Loader;
