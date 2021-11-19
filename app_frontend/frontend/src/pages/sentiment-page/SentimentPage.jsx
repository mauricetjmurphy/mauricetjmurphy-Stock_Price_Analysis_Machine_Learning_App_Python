import React, { useState } from "react";
import styled from "styled-components";
import SideNavbar from "../../components/SideNavbar";
import Loader from "../../components/Loader";
import axios from "axios";
import Plot from "react-plotly.js";
import * as d3 from "d3";

const SentimentContainer = styled.section`
    display: flex;
`;

const GrpahContainer = styled.section`
    flex: 10;
`;

function SentimentPage() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState();
    const [error, setError] = useState();

    const handleClick = () => {
        setLoading(true);
        const config = {
            method: "GET",
            url: "api/predictions/",
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods":
                    "GET,PUT,POST,DELETE,PATCH,OPTIONS",
            },
        };

        axios
            .request(config)
            .then(function (response) {
                console.log(response.data);
                setData(response.data);
                setLoading(false);
            })
            .catch(function (error) {
                console.error(error);
                setLoading(false);
            });
    };

    function transformData(data) {
        let plotData = [];

        let x = [];
        let y = [];
        data.map((el) => {
            x.push(el.date_of_interest);
            y.push(el.case_count);
        });
        plotData["x"] = x;
        plotData["y"] = y;

        return plotData;
    }

    return (
        <SentimentContainer>
            <SideNavbar form="sentiment" />
            <button onClick={handleClick}>Click</button>
            {loading ? (
                <>
                    <Loader />
                </>
            ) : (
                <GrpahContainer>
                    <h1>Results</h1>
                    <p>
                        The sentiment analysis is based on the last seven days
                        of tweet data
                    </p>
                    <p>
                        The general sentiment for the past seven days is neutral
                    </p>
                    <p>
                        There were a total of {data["tweet count"]} tweets
                        retrieved from the Twitter API
                    </p>
                    <Plot
                        data={[
                            {
                                type: "histogram",
                                x: data.seqlen,
                                marker: {
                                    color: "rgb(158,202,225)",
                                    opacity: 0.6,

                                    line: {
                                        color: "rgb(8,48,107)",
                                        width: 1.5,
                                    },
                                },
                            },
                        ]}
                        layout={{
                            bargap: 0.1,
                            width: 750,
                            height: 500,
                            title: "Tweet data",
                            xaxis: { title: "Word Count" },
                            yaxis: { title: "Density" },
                        }}
                    />
                    <Plot
                        data={[
                            {
                                type: "bar",
                                mode: "lines",
                                x: data["class names"],
                                y: data.counts,
                                marker: {
                                    color: ["#eb4034", "#e3820b", "#32a852"],
                                    opacity: 0.6,
                                    line: {
                                        color: "rgb(8,48,107)",
                                        width: 1.5,
                                    },
                                },
                            },
                        ]}
                        layout={{
                            width: 750,
                            height: 500,
                            title: "Sentiment data",
                            xaxis: { title: "Twitter sentiment" },
                            yaxis: { title: "Tweet count" },
                        }}
                    />
                </GrpahContainer>
            )}
        </SentimentContainer>
    );
}

export default SentimentPage;
