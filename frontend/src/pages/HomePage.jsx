import { useEffect, useState } from "react";
import api from "../api";

function HomePage() {
  const [data, setData] = useState([]);

  // Alimenta-se da api e obtem os filmes salvos no banco de dados.
  async function fetchFilms() {
    try {
      const res = await api.get("/films/");
      setData(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    async function load() {
      try {
        const res = await fetchFilms();
        setData(res.data);
      } catch (err) {
        console.error(err);
      }
    }

    load();
  }, []);

  console.log(data);

  return (
    <div className="">
      <h1>Home page</h1>
      {data.films?.map((film) => (
        <div key={film.id}>{film.name}</div>
      ))}
    </div>
  );
}

export default HomePage;
