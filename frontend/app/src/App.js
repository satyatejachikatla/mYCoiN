import React, { useState, useEffect } from "react";
import PostForm from "./components/PostForm";
import LedgerData from "./components/LedgerData";

function App() {
  const [initialData, setInitialData] = useState([{}]);

  useEffect(() => {
    fetch("/api")
      .then((response) => response.json())
      .then((data) => setInitialData(data));
  }, []);
  return (
    <div className="App">
      <h1>{initialData.title}</h1>
      <PostForm />
      <LedgerData />
    </div>
  );
}

export default App;
