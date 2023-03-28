import styles from "./VideoInput.module.css";

import { useState, useRef } from "react";
import UploadIcon from "@/components/icons/UploadIcon/UploadIcon";
import http from "../../../api/http-common";
import Router from "next/router";

export default function VideoInput({ width, height }) {
  const [source, setSource] = useState();
  const inputRef = useRef();

  const redirectToVideo = (r) => {
    window.location = "/" + r.data.hash;
  };

  const handleFileChange = (e) => {
    e.preventDefault();
    const file = e.target.files[0];
    let formData = new FormData();
    formData.append("file", file);
    try {
      const hash = http
        .post("upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          // onUploadProgress,
        })
        .then((r) => redirectToVideo(r));
    } catch (e) {
      console.log(e);
    } finally {
      const url = URL.createObjectURL(file);
      setSource(url);
    }
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
            accept=".mov,.mp4,.webm,.wmv,.avi,.avchd,.flv,.f4v,.swf,.mkv,.html5,.mpg,.mpeg"
          />
          <UploadIcon width={200} height={200} />
          <div className="footer">{source || "Загрузите видео"}</div>
        </button>
      )}
    </div>
  );
}
