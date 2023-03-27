import styles from "./VideoInput.module.css";

import { useState, useRef } from "react";
import UploadIcon from "@/components/icons/UploadIcon/UploadIcon";
import http from "../../../api/http-common";

export default function VideoInput({ width, height }) {
  const [source, setSource] = useState();
  const inputRef = useRef();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    let formData = new FormData();
    formData.append("file", file);

    http.post("upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      // onUploadProgress,
    });
    // axios.post("upload", formData, {
    //   headers: {
    //     "Content-Type": "multipart/form-data",
    //   },
    // });

    const url = URL.createObjectURL(file);
    setSource(url);
  };

  const handleChoose = (e) => {
    inputRef.current.click();
  };

  return (
    <div className={styles.container}>
      {source ? (
        <>
          <video controls src={source} />
          {source}
        </>
      ) : (
        <button onClick={handleChoose} className={styles.upload}>
          <input
            ref={inputRef}
            type="file"
            onChange={handleFileChange}
            accept=".mov,.mp4"
          />
          <UploadIcon width={200} height={200} />
          <div className="footer">{source || "Загрузите видео"}</div>
        </button>
      )}
    </div>
  );
}
