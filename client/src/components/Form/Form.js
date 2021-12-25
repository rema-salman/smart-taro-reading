import React, { useState } from "react";

import styles from "./Form.module.css";

const Form = ({ submitSearch, words }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [error, seterror] = useState(false);
  const onSubmit = (e) => {
    e.preventDefault();
    if (!searchQuery || searchQuery === "") {
      seterror("Please write your question, so the reading can be done.");
      return;
    }
    seterror(false);
    submitSearch(searchQuery);
    setSearchQuery("");
  };

  return (
    <form className={styles.form} onSubmit={onSubmit}>
      <h1 className={styles.heading}>
        Smart <span className={styles.light}> Taro Reading</span>
      </h1>

      {error && <p className={styles.errorMsg}>{error}</p>}
      {/* Random words */}
      {words && words.length > 0 ? (
        <div>
          <p className={styles.errorMsg}>
            Please construct a question using one or several words of the
            following list
          </p>
          {words.map((word, index) => (
            <li key={index}>{word}</li>
          ))}
        </div>
      ) : (
        ""
      )}
      <input
        aria-label="searchQuery"
        type="textarea"
        className={`${styles.input} d-flex flex-wrap form-control`}
        placeholder="Ask something ..."
        required
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      <button
        className={`btn btn-lg ${styles.button}`}
        type="submit"
        onClick={onSubmit}
      >
        Read my Fortune
      </button>
    </form>
  );
};

export default Form;
