import React, { useState } from "react";

const Chatbot = () => {
    const [userQuery, setUserQuery] = useState("");
    const [chatResponse, setChatResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const handleQuerySubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setChatResponse("");

        try {
            const response = await fetch("http://127.0.0.1:8000/chatbot/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query: userQuery }),
            });

            if (!response.ok) {
                throw new Error("Failed to fetch chatbot response");
            }

            const data = await response.json();
            setChatResponse(data.results || "No results found.");
        } catch (error) {
            setChatResponse("Error: " + error.message);
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
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Loading..." : "Ask"}
                </button>
            </form>
            <div>
                <h3>Response:</h3>
                <pre>{typeof chatResponse === "string" ? chatResponse : JSON.stringify(chatResponse, null, 2)}</pre>
            </div>
        </div>
    );
};

export default Chatbot;
