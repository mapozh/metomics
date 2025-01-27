import React, { useState } from "react";

const Chatbot = () => {
    const [userQuery, setUserQuery] = useState("");
    const [chatResponse, setChatResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleQuerySubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setChatResponse(null);

        try {
            const response = await fetch("http://127.0.0.1:8000/chatbot/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query: userQuery }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to fetch chatbot response.");
            }

            const data = await response.json();

            // Ensure the response is properly set
            if (data.response) {
                setChatResponse(data.response);
            } else {
                setChatResponse("No response received from chatbot.");
            }
        } catch (error) {
            setChatResponse(`Error: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Chatbot Interface</h2>
            <form onSubmit={handleQuerySubmit}>
                <input
                    type="text"
                    value={userQuery}
                    onChange={(e) => setUserQuery(e.target.value)}
                    placeholder="Ask a question about your RDF data..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !userQuery.trim()}>
                    {loading ? "Loading..." : "Ask"}
                </button>
            </form>
            <div>
                <h3>Response:</h3>
                {chatResponse ? (
                    <pre>{chatResponse}</pre>
                ) : (
                    <p>{loading ? "Waiting for response..." : "No response yet."}</p>
                )}
            </div>
        </div>
    );
};

export default Chatbot;
