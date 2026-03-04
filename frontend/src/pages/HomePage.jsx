import { useEffect, useState } from "react";
import api from "../api";

function HomePage() {
  const [films, setFilms] = useState([]);
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    // Função para puxar os filmes
    async function fetchFilms() {
      try {
        const res = await api.get("/films/");
        setFilms(res.data.films);
      } catch (err) {
        console.error(err);
      }
    }

    // Função para puxar as sessões
    async function fetchSessions() {
      try {
        const res = await api.get("/sessions/");
        setSessions(res.data.sessions)
      } catch (err) {
        console.error(err);
      }
    }

    fetchFilms()
    fetchSessions()
  }, []);

  return (
    <div className="grid grid-cols-2">
      <div className="flex flex-col w-lg bg-zinc-900 p-2">
        <h1>Card de Filme</h1>

        {/* Exemplo de list dos filmes */}
        {films?.map((film) => (

          <div key={film.id} className="flex flex-col gap-2 bg-zinc-700 p-2">

            <h1>Nome: {film.name}</h1>

            <p>Descrição: {film.description}</p>

            <p>Duração: {film.duration}</p>

            <p>Diretor: {film.director}</p>
            
            <p>Elenco: {film.movie_cast}</p>

            <p>Classificação Indicativa: {film.age_rating}</p>

            <p>Visibilidade: {film.display_label}</p>
            
            <div className="flex gap-2">
              <p>Gêneros: </p>
              {film.film_genre.map((genre) => {
                return <span key={genre.id}>{genre.name}</span>
              })}
            </div>

            <img src={`http://localhost:8000${film.thumb_image}`} alt="" />

            <img src={`http://localhost:8000${film.banner_image}`} alt="" />
          </div>
        ))}
      </div>

      <div className="flex flex-col w-lg bg-zinc-900 p-2">
        <h1>Card de Sessão</h1>

        {/* Exemplo de list dos filmes */}
        {sessions?.map((session) => (

          <div key={session.id} className="flex flex-col gap-2 bg-zinc-700 p-2">

            <h1>Nome: {session.name}</h1>

            <p>Descrição: {session.film}</p>

            <div className="flex gap-2">
              {Object.entries(session.catg_grouped || {}).map(([type, categories]) => (
                <div key={type}>
                  <p>{type}</p>

                  {categories.map((category) => (
                    <span key={category.id}>{category.name}</span>
                  ))}
                </div>
              ))}
            </div>

            <p>{session.week_day}</p>

            <p>{session.date}</p>

            <p>{session.room}</p>

            <p>Compra: {session.ticket_url}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
