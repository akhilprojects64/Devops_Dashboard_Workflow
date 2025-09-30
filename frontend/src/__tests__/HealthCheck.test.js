import axios from "axios";
import { render, screen, waitFor } from "@testing-library/react";
import React, { useEffect, useState } from "react";


function HealthCheck() {
  const [status, setStatus] = useState("");

  useEffect(() => {
    axios.get("/health").then(res => setStatus(res.data.status));
  }, []);

  return <div>{status ? `Status: ${status}` : "Loading..."}</div>;
}


jest.mock("axios");

test("fetches and displays health status", async () => {
  axios.get.mockResolvedValueOnce({ data: { status: "healthy" } });

  render(<HealthCheck />);

 
  expect(screen.getByText(/Loading/i)).toBeInTheDocument();

 
  await waitFor(() => {
    expect(screen.getByText(/Status: healthy/i)).toBeInTheDocument();
  });
});
