import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import StockForm from "./StockForm.jsx";
import SentimentForm from "./SentimentForm.jsx";

const SidebarContainer = styled.section`
    min-height: calc(100vh - 120px);
    flex: 2;
    background: #344a5e;
    color: #9aa5ae;
`;

const DashbordContainer = styled.div`
    display: flex;
    height: 60px;
    border-bottom: 1px solid #9aa5ae47;

    h1 {
        margin: 0;
        padding: 15px 0 15px 30px;
    }
`;

const FormContainer = styled.div`
    height: calc(100vh - 430px);
    display: flex;
    align-items: center;
    padding-left: 30px;
`;

const TabContainer = styled.ul`
    display: flex;
    flex-direction: column;
    padding: 0;
`;

const LinkContainer = styled(Link)`
    height: 50px;
    list-style: none;
    text-align: left;
    border-bottom: 1px solid #9aa5ae47;
    padding-left: 30px;
    line-height: 50px;
    text-decoration: none;
    color: #9aa5ae;

    &:hover {
        background: #ffffff45;
        cursor: pointer;
    }

    &:first-child {
        border-top: 1px solid #9aa5ae47;
    }
`;

function SideNavbar({ form }) {
    return (
        <SidebarContainer>
            <DashbordContainer>
                <h1>Dashbord</h1>
            </DashbordContainer>
            <FormContainer>
                {form == "Stock" ? <StockForm /> : <SentimentForm />}
            </FormContainer>
            <TabContainer>
                <LinkContainer to="/">Stock Analysis</LinkContainer>
                <LinkContainer to="/sentiment">
                    Sentiment Analysis
                </LinkContainer>
            </TabContainer>
        </SidebarContainer>
    );
}

export default SideNavbar;
