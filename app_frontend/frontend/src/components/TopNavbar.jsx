import React, { useState } from "react";
import styled from "styled-components";

const TopNavbarContainer = styled.section`
    height: 80px;
    max-width: 100vw;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
    background: #5b90bf;
    color: #fff;
`;

const BrandContainer = styled.div`
    display: flex;
    align-items: flex-end;

    p {
        padding: 0 0 5px 15px;
    }
`;

const Logout = styled.a`
    &:hover {
        color: #000;
        cursor: pointer;
    }
`;

function TopNavbar() {
    const [name, setname] = useState();

    return (
        <TopNavbarContainer>
            <BrandContainer>
                <h1>StockZip</h1>
                <p>Hi, {name}</p>
            </BrandContainer>
            <div>
                <Logout>Logout</Logout>
            </div>
        </TopNavbarContainer>
    );
}

export default TopNavbar;
