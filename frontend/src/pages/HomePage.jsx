import { useEffect, useState } from "react";
import api from "../api";

function HomePage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await api.get("/test/");
        setData(res.data);
      } catch (err) {
        console.error(err);
      }
    }

    fetchData();
  }, []);

  return (
    <div className="">
      <h1>Home page</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default HomePage;
