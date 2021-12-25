import React, { Fragment } from "react";

import useFetchCards from "./hooks/useFetchCards";

import Form from "./components/Form";
import Error from "./components/Error";
import BubbleLoader from "./components/BubbleLoader";

function App() {
  const { cards, words, loading, error, submitRequest } = useFetchCards();

  function onSubmit(value) {
    submitRequest(value);
  }

  return (
    <Fragment>
      {/* Error */}
      {error && <Error error={error} />}
      {/* Loader */}
      {loading && <BubbleLoader />}
      {/* Form */}
      <Form submitSearch={onSubmit} words={words} />

      {/* Images container */}
      {cards && cards.length > 0 ? (
        <div className="d-flex flex-column">
          <h3 style={{ textAlign: "center" }}>YOUR READINGS</h3>
          <div className="d-flex m-5 justify-content-around align-items-center flex-wrap">
            {cards.map((card) => (
              <div key={card.number} className="card m-4">
                <img
                  className="card-img-top"
                  src={`/cards/${card.img}`}
                  alt={card.name}
                />
                <div className="card-body">
                  <h1 className="card-title">{card.name}</h1>
                  {card.fortune_telling.map((item, index) => (
                    <p key={index} className="card-text">
                      {item}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        ""
      )}
    </Fragment>
  );
}

export default App;
