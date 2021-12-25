import { useState } from "react";
import axios from "axios";

const BASE_URL = "http://localhost:5000/cards";

export default function useFetchCards() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [cards, setCards] = useState([]);
  const [words, setWords] = useState([]);
  const submitRequest = (query) => {
    setError(false);
    setLoading(true);
    setWords([]);
    setCards([]);

    // get data from server
    axios
      .get(`${BASE_URL}`, {
        params: {
          query,
        },
      })
      .then((res) => {
        console.log(res.data);
        //  response with matching cards
        if (res.data.length === 3) {
          setLoading(false);
          setCards(res.data);
        } else {
          // response with random words
          setLoading(false);
          setWords(res.data);
        }
      })
      .catch((e) => {
        setLoading(false);
        setError("Something went wrong, please try again..");
      });
  };

  return {
    cards,
    words,
    loading,
    error,
    submitRequest,
  };
}
