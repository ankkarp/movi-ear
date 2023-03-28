import axios from "axios";

export default axios.create({
  baseURL: process.env.SERVER,
  headers: {
    "Content-type": "application/json",
  },
});
