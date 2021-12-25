import React from "react";
import Loader from "react-js-loader";

function BubbleLoader() {
  return (
    <div
      className="d-flex justify-content-around align-items-center"
      style={{ height: "100vh" }}
    >
      <Loader type="bubble-scale" bgColor={"#DB2200"} size={400} />
    </div>
  );
}

export default BubbleLoader;
