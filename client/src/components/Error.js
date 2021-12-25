import React, { useState } from "react";

function Error({ error }) {
  return (
    <div
      className="d-flex flex-column justify-content-around align-items-center"
      style={{ height: "30vh" }}
    >
      <h1 style={{ color: "#db2200" }}>{error}</h1>
    </div>
  );
}

export default Error;
